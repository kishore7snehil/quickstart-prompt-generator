# Auth0 SPA JS SDK Svelte Quickstart

*This file contains the LLM response to the synthesis prompt.*

```
# Secure Authentication in Svelte with Auth0

<div class="alert alert-info">
  <strong>Quickstart for Single Page Applications (SPAs) using Svelte</strong><br>
  This quickstart guide demonstrates how to add authentication to a Svelte application using Auth0. It uses the Auth0 SPA JS SDK with the Authorization Code Grant Flow with PKCE (Proof Key for Code Exchange), which is the recommended approach for securing SPAs.
</div>

## Before You Begin

### Prerequisites

- [Node.js](https://nodejs.org) (v14.0+)
- [npm](https://npmjs.com/get-npm) (v6.0+) or [yarn](https://yarnpkg.com/)
- Basic knowledge of [Svelte](https://svelte.dev/)
- A free [Auth0 account](https://auth0.com/signup)

### What You Will Build

This tutorial shows you how to integrate Auth0 authentication into a Svelte application to:

- Set up an Auth0 application and API
- Add login, logout, and sign-up capabilities
- Display user profile information
- Protect routes from unauthorized access
- Make authenticated API calls

<div class="alert alert-success">
  <strong>Sample Code</strong><br>
  The completed code for this tutorial is available on <a href="https://github.com/auth0-samples/auth0-svelte-samples/tree/master/01-Login">GitHub</a>.
</div>

## Set Up Auth0

### Create an Auth0 Application

1. **Sign in** to the [Auth0 Dashboard](https://manage.auth0.com/)
2. In the left sidebar, click on **Applications → Applications**
3. Click the **Create Application** button
4. Enter a **Name** for your application (e.g., "My Svelte App")
5. Select **Single Page Web Applications** for application type
6. Click **Create**

### Configure Authentication Settings

1. Click on the **Settings** tab
2. Add the following URLs to the **Allowed Callback URLs** field:
   ```
   http://localhost:5000/callback, http://localhost:5000
   ```
3. Add the following URLs to the **Allowed Logout URLs** field:
   ```
   http://localhost:5000
   ```
4. Add the following URLs to the **Allowed Web Origins** field:
   ```
   http://localhost:5000
   ```
5. Scroll down and click **Save Changes**

<div class="alert alert-warning">
  <strong>Note</strong><br>
  For production applications, you'll need to add your actual domain URLs instead of localhost. Make sure to use HTTPS for production environments.
</div>

## Create Your Svelte Application

If you already have a Svelte application, you can skip this step. Otherwise, let's create a new Svelte application using the recommended template:

```bash
npx degit sveltejs/template my-svelte-auth-app
cd my-svelte-auth-app
npm install
```

## Install Dependencies

Install the Auth0 SPA JS SDK:

```bash
npm install @auth0/auth0-spa-js
```

If you plan to create a more complete application with routing, install svelte-spa-router as well:

```bash
npm install svelte-spa-router
```

## Implement Authentication

Let's build our authentication system step-by-step.

### 1. Create an Auth0 Configuration File

Create a new file `src/auth_config.js` with your Auth0 application settings:

```javascript
// src/auth_config.js
export const authConfig = {
  domain: "YOUR_AUTH0_DOMAIN", // e.g., dev-abc12345.us.auth0.com
  clientId: "YOUR_CLIENT_ID",
  audience: "YOUR_API_IDENTIFIER", // Optional: Only needed if you will use an API
  redirectUri: window.location.origin,
  useRefreshTokens: true,
  cacheLocation: "localstorage"
};
```

<div class="alert alert-danger">
  <strong>Important</strong><br>
  Replace <code>YOUR_AUTH0_DOMAIN</code> and <code>YOUR_CLIENT_ID</code> with your actual Auth0 application values from the Auth0 Dashboard.
</div>

### 2. Create an Auth Store

Svelte's built-in stores make it perfect for managing authentication state. Create a new file `src/stores/auth.js`:

```javascript
// src/stores/auth.js
import { writable, derived } from 'svelte/store';
import createAuth0Client from '@auth0/auth0-spa-js';
import { authConfig } from '../auth_config';
import { push } from 'svelte-spa-router';

// Auth0 client store
export const auth0Client = writable(null);

// User store
export const user = writable(null);

// Loading state store
export const isLoading = writable(true);

// Authentication state store
export const isAuthenticated = derived(
  user,
  $user => $user !== null
);

// Error store
export const authError = writable(null);

// Initialize Auth0 client
export async function initializeAuth0() {
  try {
    // Create new Auth0 client
    const client = await createAuth0Client(authConfig);
    auth0Client.set(client);
    
    // Check for authentication callback and handle it
    if (window.location.search.includes("code=") && 
        window.location.search.includes("state=")) {
          
      // Handle redirect callback
      const { appState } = await client.handleRedirectCallback();
      
      // Clear the URL parameters
      window.history.replaceState({}, document.title, "/");
      
      // If we have saved app state, navigate to it
      if (appState && appState.targetUrl) {
        push(appState.targetUrl);
      }
    }
    
    // Check if user is authenticated
    const isAuth = await client.isAuthenticated();
    if (isAuth) {
      // Get user details
      const userProfile = await client.getUser();
      user.set(userProfile);
    }
  } catch (err) {
    authError.set(err);
    console.error('Error initializing Auth0', err);
  } finally {
    isLoading.set(false);
  }
}

// Login function
export async function login(redirectPath = '/') {
  try {
    const client = await getClient();
    await client.loginWithRedirect({
      appState: { targetUrl: redirectPath }
    });
  } catch (err) {
    authError.set(err);
    console.error('Log in error', err);
  }
}

// Logout function
export async function logout(returnTo = window.location.origin) {
  try {
    const client = await getClient();
    client.logout({
      returnTo
    });
  } catch (err) {
    authError.set(err);
    console.error('Log out error', err);
  }
}

// Get access token
export async function getToken(options) {
  try {
    const client = await getClient();
    return await client.getTokenSilently(options);
  } catch (err) {
    // If we get login_required, we need to prompt for login
    if (err.error === 'login_required') {
      // Save current location and redirect to login
      login(window.location.pathname);
      return null;
    }
    
    authError.set(err);
    console.error('Error getting token', err);
    return null;
  }
}

// Helper to ensure auth0Client is initialized
async function getClient() {
  let client;
  const unsubscribe = auth0Client.subscribe(value => {
    client = value;
  });
  unsubscribe();
  
  if (!client) {
    throw new Error('Auth0 client not initialized');
  }
  
  return client;
}
```

### 3. Create a Protected Route Guard

Create a file `src/guards/AuthGuard.svelte` to protect routes that require authentication:

```svelte
<!-- src/guards/AuthGuard.svelte -->
<script>
  import { onMount } from 'svelte';
  import { push } from 'svelte-spa-router';
  import { isAuthenticated, isLoading, login } from '../stores/auth';
  
  export let component;
  
  let authChecked = false;
  
  onMount(() => {
    const unsubscribeAuth = isAuthenticated.subscribe(authenticated => {
      if (!$isLoading && !authenticated && !authChecked) {
        // Save current path and redirect to login
        login(window.location.pathname);
      }
      authChecked = true;
    });
    
    return () => {
      unsubscribeAuth();
    };
  });
</script>

{#if $isLoading}
  <div class="loading">
    <p>Loading authentication...</p>
  </div>
{:else if $isAuthenticated}
  <svelte:component this={component} />
{/if}
```

### 4. Create Authentication UI Components

Let's create a few key components for our authentication UI.

#### Login Button

Create `src/components/LoginButton.svelte`:

```svelte
<!-- src/components/LoginButton.svelte -->
<script>
  import { login } from '../stores/auth';
</script>

<button on:click={() => login()}>
  Log in
</button>
```

#### Logout Button

Create `src/components/LogoutButton.svelte`:

```svelte
<!-- src/components/LogoutButton.svelte -->
<script>
  import { logout } from '../stores/auth';
</script>

<button on:click={() => logout()}>
  Log out
</button>
```

#### User Profile Component

Create `src/components/Profile.svelte`:

```svelte
<!-- src/components/Profile.svelte -->
<script>
  import { user } from '../stores/auth';
</script>

{#if $user}
  <div class="profile">
    <div class="profile-header">
      {#if $user.picture}
        <img src={$user.picture} alt="Profile" class="profile-picture" />
      {/if}
      <h2>{$user.name}</h2>
    </div>
    <div class="profile-details">
      <p><strong>Email:</strong> {$user.email}</p>
      <p><strong>Email verified:</strong> {$user.email_verified ? 'Yes' : 'No'}</p>
      <pre class="json">{JSON.stringify($user, null, 2)}</pre>
    </div>
  </div>
{:else}
  <p>No user information available</p>
{/if}

<style>
  .profile {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  .profile-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
  }
  .profile-picture {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    margin-right: 20px;
    object-fit: cover;
  }
  .json {
    background: #f5f5f5;
    padding: 15px;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 12px;
  }
</style>
```

### 5. Create Pages

Let's set up some basic pages for our app.

#### Home Page

Create `src/pages/Home.svelte`:

```svelte
<!-- src/pages/Home.svelte -->
<script>
  import { isAuthenticated } from '../stores/auth';
  import LoginButton from '../components/LoginButton.svelte';
  import LogoutButton from '../components/LogoutButton.svelte';
</script>

<div class="home">
  <h1>Welcome to Svelte Auth0 Demo</h1>
  
  <p>
    This example shows how to add authentication to a Svelte application using Auth0.
  </p>
  
  {#if $isAuthenticated}
    <p>You are logged in! You can now:</p>
    <ul>
      <li><a href="/#/profile">View your profile</a></li>
      <li><a href="/#/api">Call an API</a></li>
    </ul>
    <LogoutButton />
  {:else}
    <p>You are not logged in! Please log in to continue.</p>
    <LoginButton />
  {/if}
</div>

<style>
  .home {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
  }
  ul {
    list-style-type: none;
    padding: 0;
    margin: 20px 0;
  }
  li {
    margin-bottom: 10px;
  }
  a {
    color: #ff3e00;
    text-decoration: none;
  }
  a:hover {
    text-decoration: underline;
  }
</style>
```

#### Profile Page

Create `src/pages/ProfilePage.svelte`:

```svelte
<!-- src/pages/ProfilePage.svelte -->
<script>
  import Profile from '../components/Profile.svelte';
</script>

<div class="page">
  <h1>User Profile</h1>
  <Profile />
  <p><a href="/#/">← Back to Home</a></p>
</div>

<style>
  .page {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  a {
    color: #ff3e00;
    text-decoration: none;
  }
  a:hover {
    text-decoration: underline;
  }
</style>
```

#### API Demo Page

Create `src/pages/ApiDemo.svelte` to demonstrate calling a protected API:

```svelte
<!-- src/pages/ApiDemo.svelte -->
<script>
  import { onMount } from 'svelte';
  import { getToken } from '../stores/auth';
  
  let apiMessage = '';
  let error = null;
  let loading = false;
  
  async function callApi() {
    loading = true;
    apiMessage = '';
    error = null;
    
    try {
      // Get the access token
      const token = await getToken({
        authorizationParams: {
          audience: 'YOUR_API_IDENTIFIER' // Use the same audience as in auth_config.js
        }
      });
      
      if (!token) {
        throw new Error('Could not get access token');
      }
      
      // Call your API
      const response = await fetch('https://your-api-url/api/protected', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || 'API call failed');
      }
      
      apiMessage = data.message || JSON.stringify(data);
    } catch (err) {
      error = err.message;
      console.error('API call error', err);
    } finally {
      loading = false;
    }
  }
</script>

<div class="page">
  <h1>API Demo</h1>
  
  <p>
    This page demonstrates how to use an access token to call a protected API.
    Click the button below to make an authenticated API call.
  </p>
  
  <button on:click={callApi} disabled={loading}>
    {loading ? 'Loading...' : 'Call API'}
  </button>
  
  {#if apiMessage}
    <div class="result success">
      <h3>Result</h3>
      <p>{apiMessage}</p>
    </div>
  {/if}
  
  {#if error}
    <div class="result error">
      <h3>Error</h3>
      <p>{error}</p>
    </div>
  {/if}
  
  <p><a href="/#/">← Back to Home</a></p>
</div>

<style>
  .page {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  button {
    background: #ff3e00;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
  }
  button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
  .result {
    margin-top: 20px;
    padding: 15px;
    border-radius: 4px;
  }
  .success {
    background: #e7f7e7;
    border: 1px solid #5cb85c;
  }
  .error {
    background: #f8d7da;
    border: 1px solid #dc3545;
  }
  a {
    color: #ff3e00;
    text-decoration: none;
  }
  a:hover {
    text-decoration: underline;
  }
</style>
```

<div class="alert alert-warning">
  <strong>Note</strong><br>
  Replace <code>YOUR_API_IDENTIFIER</code> and <code>https://your-api-url/api/protected</code> with your actual API values. If you don't have an API set up, you can skip this step or refer to the Auth0 API documentation.
</div>

### 6. Set Up Routing

Create a router configuration in `src/routes.js`:

```javascript
// src/routes.js
import Home from './pages/Home.svelte';
import ProfilePage from './pages/ProfilePage.svelte';
import ApiDemo from './pages/ApiDemo.svelte';
import AuthGuard from './guards/AuthGuard.svelte';

export const routes = {
  '/': Home,
  '/profile': {
    component: AuthGuard,
    props: {
      component: ProfilePage
    }
  },
  '/api': {
    component: AuthGuard,
    props: {
      component: ApiDemo
    }
  },
  '*': Home
};
```

### 7. Update the App Component

Update `src/App.svelte` to use our authentication system and router:

```svelte
<!-- src/App.svelte -->
<script>
  import { onMount } from 'svelte';
  import Router from 'svelte-spa-router';
  import { routes } from './routes';
  import { initializeAuth0, isLoading } from './stores/auth';
  
  onMount(async () => {
    // Initialize the Auth0 client
    await initializeAuth0();
  });
</script>

<main>
  {#if $isLoading}
    <div class="loading">
      <p>Loading application...</p>
    </div>
  {:else}
    <Router {routes} />
  {/if}
</main>

<style>
  main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 16px;
  }
  .loading {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
</style>
```

## Run Your Application

Now that we've set up authentication, let's run the application:

```bash
npm run dev
```

Your application should now be running on [http://localhost:5000](http://localhost:5000).

## Test Authentication Flow

1. Navigate to the home page
2. Click "Log in" to authenticate with Auth0
3. After successful authentication, you'll be redirected back
4. You should now see your user information and be able to access protected routes
5. Try accessing the Profile page and API Demo page
6. Click "Log out" to end your session

## Error Handling

Our implementation includes error handling for common scenarios:

- **Network issues**: Failed API calls are caught and displayed
- **Authentication errors**: Problems with login/logout are caught and logged
- **Token errors**: Issues with token acquisition are handled gracefully
- **Route protection**: Unauthorized access attempts redirect to login

For a more comprehensive error handling system, consider implementing:

1. A global error notification component
2. More detailed logging
3. Retry mechanisms for token acquisition
4. Custom error pages for different authentication states

## Advanced Usage

### Customizing the Login Experience

You can customize the Auth0 login page by passing options to the `loginWithRedirect` function:

```javascript
await client.loginWithRedirect({
  authorizationParams: {
    screen_hint: 'signup',  // Direct users to signup page
    prompt: 'login',        // Force re-authentication
    login_hint: 'user@example.com' // Pre-fill email field
  },
  appState: { targetUrl: '/dashboard' } // Where to redirect after login
});
```

### Accessing Additional User Information

If you need more user information than what's included in the ID token, you can use the Auth0 Management API. You'll need to request the appropriate scopes and set up an API in the Auth0 Dashboard.

### Role-Based Access Control

For role-based access control, you can use Auth0 roles and permissions:

1. Set up roles in the Auth0 Dashboard
2. Assign roles to users
3. Request the `roles` scope in your application
4. Check for roles in the user's access token

## Next Steps

- **Set up an actual API** using Auth0 for authentication
- **Configure Silent Authentication** for a better user experience
- **Add Auth0 Actions** for custom login/signup logic
- **Set up Social Connections** to enable social login
- **Implement MFA** (Multi-Factor Authentication) for added security

## Additional Resources

- [Auth0 SPA SDK Documentation](https://auth0.com/docs/libraries/auth0-spa-js)
- [Auth0 Svelte Samples](https://github.com/auth0-samples/auth0-svelte-samples)
- [Svelte Documentation](https://svelte.dev/docs)
- [Auth0 Blog - Svelte Articles](https://auth0.com/blog/search/?query=svelte)
- [Auth0 Community](https://community.auth0.com/)

## Troubleshooting

### Common Issues

#### "Login required" error when getting token

This happens when your session has expired. Our implementation automatically redirects to login when this occurs.

#### Popup blocked by browser

If using popup authentication, ensure popups are allowed for your domain.

#### "Invalid state" error after login

This typically happens with expired authentication requests or when the callback URL is not configured correctly in Auth0.

#### CORS errors when calling API

Ensure your API's CORS settings allow requests from your application domain.

## Conclusion

## Next Steps

Excellent work! If you made it this far, you should now have login, logout, and user profile information running in your Svelte application.

This concludes our quickstart tutorial, but there is so much more to explore. To learn more about what you can do with Auth0, check out:

**Auth0 Dashboard & Management**
- [Auth0 Dashboard](https://manage.auth0.com/) - Learn how to configure and manage your Auth0 tenant and applications
- [Auth0 Marketplace](https://marketplace.auth0.com/) - Discover integrations you can enable to extend Auth0's functionality

**SDK Resources**
- [auth0-spa-js SDK](https://github.com/auth0/auth0-spa-js) - Explore the SDK used in this tutorial more fully
- [SDK Documentation](https://auth0.github.io/auth0-spa-js/) - Complete API reference and advanced configuration options
- [Examples Repository](https://github.com/auth0/auth0-spa-js/tree/main/examples) - Additional implementation examples

**Advanced Implementation**
- [Svelte Authentication By Example](https://developer.auth0.com/resources/guides/spa/svelte/basic-authentication) - Deep dive into implementing user authentication in Svelte
- [Protected Routes in SPAs](https://auth0.com/docs/quickstart/spa/vanillajs/02-calling-an-api) - Learn how to protect routes and call APIs
- [Organizations](https://auth0.com/docs/organizations) - Implement multi-tenant applications
- [Custom Domains](https://auth0.com/docs/custom-domains) - Use your own domain for the Auth0 Universal Login

**Community & Support**
- [Auth0 Community](https://community.auth0.com/) - Get help from the Auth0 community
- [Svelte Discord](https://discord.gg/svelte) - Connect with other Svelte developers
- [GitHub Issues](https://github.com/auth0/auth0-spa-js/issues) - Report bugs or request features

**Security Best Practices**
- [Security Best Practices](https://auth0.com/docs/security/security-best-practices) - Learn about securing your applications
- [Token Best Practices](https://auth0.com/docs/security/tokens/token-best-practices) - Handle tokens securely
- [CORS Configuration](https://auth0.com/docs/cross-origin-authentication) - Configure CORS for your application

### Sample Application

You can find a complete working example of this quickstart in our [Svelte sample application repository](https://github.com/auth0-samples/auth0-svelte-samples).

### Troubleshooting

**Common Issues:**

1. **"Invalid state" error**: Make sure your callback URL is configured correctly in the Auth0 Dashboard
2. **CORS errors**: Ensure your domain is added to "Allowed Web Origins" in Auth0 Dashboard
3. **Token refresh issues**: Check that `useRefreshTokens: true` is set and refresh tokens are enabled for your application
4. **Popup blocked**: Some browsers block popups by default - consider using redirect flow instead

**Getting Help:**

If you encounter issues not covered in this guide:
1. Check the [Auth0 Community](https://community.auth0.com/) for similar questions
2. Review the [SDK documentation](https://auth0.github.io/auth0-spa-js/) for detailed API information
3. Open an issue in the [GitHub repository](https://github.com/auth0/auth0-spa-js/issues) if you find a bug

---

*Did this help you get started with Auth0 in your Svelte application? We'd love to hear your feedback in the [Auth0 Community](https://community.auth0.com/)!*- [ ] External service setup is thoroughly explained
- [ ] Error handling and troubleshooting is addressed
- [ ] Follows Auth0 documentation style patterns
- [ ] Matches Svelte best practices

## LLM Response Ends here

## Developer Check List
- [ ] Formatting is consistent with Auth0 standards
- [ ] All code snippets have been tested
- [ ] Links to additional resources are included
- [ ] Documentation follows the style guide patterns
- [ ] All mandatory quality requirements are met


