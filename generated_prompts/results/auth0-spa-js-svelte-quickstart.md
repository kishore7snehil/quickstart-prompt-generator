# Auth0 SPA JS SDK Svelte Quickstart

*This file contains the LLM response to the synthesis prompt.*

# Add Login to your Svelte Application

Auth0 allows you to add authentication to almost any application type quickly. This guide demonstrates how to integrate Auth0, add authentication, and display user profile information in any Svelte application using the [Auth0 SPA JS SDK](https://github.com/auth0/auth0-spa-js).

To use this quickstart, you'll need to:

- Sign up for a free Auth0 account or log in to Auth0.
- Have a working Svelte project that you want to integrate with. Alternatively, you can view or download a sample application after logging in.

## 1. Configure Auth0

To use Auth0 services, you'll need to have an application set up in the Auth0 Dashboard. The Auth0 application is where you will configure how you want authentication to work for the project you are developing.

### Configure an application

Use the interactive selector to create a new Auth0 application or select an existing application that represents the project you want to integrate with.

Every application in Auth0 is assigned an alphanumeric, unique client ID that your application code will use to call Auth0 APIs through the SDK.

Any settings you configure using this quickstart will automatically update for your Auth0 application in the Dashboard, which you can always view or edit by going to the [Applications section](https://manage.auth0.com/#/applications) of the Auth0 Dashboard.

### Configure Callback URLs

A callback URL is a URL in your application that you would like Auth0 to redirect users to after they have authenticated. If not set, users will not be returned to your application after they log in.

Set the following as your callback URL:

```
http://localhost:5173
```

### Configure Logout URLs  

A logout URL is a URL in your application that you would like Auth0 to redirect users to after they have logged out. If not set, users will not be redirected to any specific URL after logging out.

Set the following as your logout URL:

```
http://localhost:5173
```

### Configure Allowed Web Origins

You need to allow your Svelte application's origin in the Auth0 settings. If not set, the application will be unable to silently refresh the authentication tokens and your users will be logged out the next time they visit the application, or refresh the page.

Set the following as your allowed web origin:

```
http://localhost:5173
```

## 2. Install the Auth0 SPA JS SDK

Auth0 provides a [SPA JS SDK](https://github.com/auth0/auth0-spa-js) to simplify the process of implementing Auth0 authentication and authorization in Single Page Applications.

Install the Auth0 SPA JS SDK by running the following command in your terminal:

```bash
npm install @auth0/auth0-spa-js
```

The SDK exposes several methods that help integrate Auth0 in a Svelte application idiomatically, including client initialization and authentication methods.

## 3. Configure the Auth0 Client

Now you will create an Auth0 configuration file and set up the Auth0 client. The Auth0 client is the primary interface for your app to communicate with Auth0.

Create a file called `auth.js` in your `src/lib` directory:

```javascript
// src/lib/auth.js
import { createAuth0Client } from '@auth0/auth0-spa-js';
import { writable } from 'svelte/store';

// Auth0 configuration
const config = {
  domain: 'YOUR_AUTH0_DOMAIN',
  clientId: 'YOUR_AUTH0_CLIENT_ID',
  authorizationParams: {
    redirect_uri: window.location.origin,
    scope: 'openid profile email'
  },
  useRefreshTokens: true,
  cacheLocation: 'localstorage'
};

// Svelte stores for auth state
export const auth0Client = writable(null);
export const isLoading = writable(true);
export const isAuthenticated = writable(false);
export const user = writable(null);
export const authError = writable(null);

// Initialize Auth0 client
export async function initializeAuth0() {
  try {
    const client = await createAuth0Client(config);
    auth0Client.set(client);
    
    // Check if user is already authenticated
    const authenticated = await client.isAuthenticated();
    isAuthenticated.set(authenticated);
    
    if (authenticated) {
      const userData = await client.getUser();
      user.set(userData);
    }
  } catch (error) {
    authError.set(error);
    console.error('Error initializing Auth0:', error);
  } finally {
    isLoading.set(false);
  }
}

// Handle redirect callback
export async function handleRedirectCallback() {
  try {
    const client = await createAuth0Client(config);
    await client.handleRedirectCallback();
    
    const authenticated = await client.isAuthenticated();
    isAuthenticated.set(authenticated);
    
    if (authenticated) {
      const userData = await client.getUser();
      user.set(userData);
    }
    
    // Remove the code and state from the URL
    window.history.replaceState({}, document.title, window.location.pathname);
  } catch (error) {
    authError.set(error);
    console.error('Error handling redirect callback:', error);
  }
}
```

Replace `YOUR_AUTH0_DOMAIN` and `YOUR_AUTH0_CLIENT_ID` with your actual Auth0 domain and client ID from your Auth0 Dashboard.

Update your main `App.svelte` file to initialize the Auth0 client:

```svelte
<!-- src/App.svelte -->
<script>
  import { onMount } from 'svelte';
  import { initializeAuth0, handleRedirectCallback, isLoading } from './lib/auth.js';
  import LoginButton from './lib/LoginButton.svelte';
  import LogoutButton from './lib/LogoutButton.svelte';
  import Profile from './lib/Profile.svelte';

  onMount(async () => {
    // Check if this is a redirect callback
    if (window.location.search.includes('code=') && window.location.search.includes('state=')) {
      await handleRedirectCallback();
    } else {
      await initializeAuth0();
    }
  });
</script>

<main>
  <h1>My Svelte App with Auth0</h1>
  
  {#if $isLoading}
    <p>Loading...</p>
  {:else}
    <LoginButton />
    <LogoutButton />
    <Profile />
  {/if}
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }
</style>
```

## 4. Add login to your application

Now that you have configured your Auth0 Application and the Auth0 SPA JS SDK, you need to set up login for your project. To do this, you will use the SDK's `loginWithRedirect()` method to redirect users to the Auth0 Universal Login page where Auth0 can authenticate them. After a user successfully authenticates, they will be redirected to your application and the callback URL you set up earlier in this quickstart.

Create a login button component in your application that calls `loginWithRedirect()` when selected.

Create a new file called `LoginButton.svelte` in your `src/lib` directory:

```svelte
<!-- src/lib/LoginButton.svelte -->
<script>
  import { auth0Client, isAuthenticated, authError } from './auth.js';

  async function login() {
    try {
      const client = $auth0Client;
      if (client) {
        await client.loginWithRedirect({
          authorizationParams: {
            screen_hint: 'signup' // Optional: show signup by default
          }
        });
      }
    } catch (error) {
      authError.set(error);
      console.error('Login error:', error);
    }
  }
</script>

{#if !$isAuthenticated}
  <button on:click={login} class="btn btn-primary">
    Log In
  </button>
{/if}

<style>
  .btn {
    background-color: #007bff;
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
  }

  .btn:hover {
    background-color: #0056b3;
  }
</style>
```

### ✅ Checkpoint

You should now be able to log in to your application.

Run your application and select the login button. Verify that:

- Your Svelte application redirects you to the Auth0 Universal Login page.
- You can log in or sign up using a username and password.
- Auth0 redirects you back to your application using the callback URL you configured.
- You do not receive any errors in the console related to Auth0.

## 5. Add logout to your application

Now that you can log in to your application, you need to add a way for your users to log out. Create a logout button using the Auth0 SPA JS SDK's `logout()` method.

Create a new file called `LogoutButton.svelte` in your `src/lib` directory:

```svelte
<!-- src/lib/LogoutButton.svelte -->
<script>
  import { auth0Client, isAuthenticated, user, authError } from './auth.js';

  async function logout() {
    try {
      const client = $auth0Client;
      if (client) {
        await client.logout({
          logoutParams: {
            returnTo: window.location.origin
          }
        });
        // Clear local state
        isAuthenticated.set(false);
        user.set(null);
      }
    } catch (error) {
      authError.set(error);
      console.error('Logout error:', error);
    }
  }
</script>

{#if $isAuthenticated}
  <button on:click={logout} class="btn btn-secondary">
    Log Out
  </button>
{/if}

<style>
  .btn {
    background-color: #6c757d;
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
  }

  .btn:hover {
    background-color: #545b62;
  }
</style>
```

### ✅ Checkpoint

Run your application and verify that:

- The **Log Out** button displays when you are logged in.
- You can click it to log out of the application.
- The **Log In** button displays when you are logged out.

## 6. Show User Profile Information

Now that your users can log in and log out, you will likely want to be able to retrieve the [profile information](https://auth0.com/docs/users/concepts/overview-user-profile) associated with authenticated users. For example, you may want to be able to display a logged-in user's name or profile picture in your application.

The Auth0 SPA JS SDK provides user information through the `getUser()` method. When a user authenticates, Auth0 returns some basic information such as the user's name, email, and profile picture. You can view a [sample user profile object from a regular web app](https://auth0.com/docs/users/references/user-profile-structure#sample-user-profile-object).

Create a new file called `Profile.svelte` in your `src/lib` directory:

```svelte
<!-- src/lib/Profile.svelte -->
<script>
  import { user, isAuthenticated, auth0Client } from './auth.js';
  import { onMount } from 'svelte';

  let idTokenClaims = null;

  onMount(async () => {
    if ($isAuthenticated && $auth0Client) {
      try {
        // Get additional ID token claims if needed
        idTokenClaims = await $auth0Client.getIdTokenClaims();
      } catch (error) {
        console.error('Error fetching ID token claims:', error);
      }
    }
  });

  // Reactive statement to update claims when auth state changes
  $: if ($isAuthenticated && $auth0Client) {
    (async () => {
      try {
        idTokenClaims = await $auth0Client.getIdTokenClaims();
      } catch (error) {
        console.error('Error fetching ID token claims:', error);
      }
    })();
  }
</script>

{#if $isAuthenticated && $user}
  <div class="profile-container">
    <h2>User Profile</h2>
    
    <div class="profile-card">
      {#if $user.picture}
        <img src={$user.picture} alt="Profile" class="profile-picture" />
      {/if}
      
      <div class="profile-info">
        <p><strong>Name:</strong> {$user.name || 'Not provided'}</p>
        <p><strong>Email:</strong> {$user.email || 'Not provided'}</p>
        <p><strong>Email Verified:</strong> {$user.email_verified ? 'Yes' : 'No'}</p>
        <p><strong>User ID:</strong> {$user.sub}</p>
        
        {#if $user.nickname}
          <p><strong>Nickname:</strong> {$user.nickname}</p>
        {/if}
        
        {#if $user.updated_at}
          <p><strong>Last Updated:</strong> {new Date($user.updated_at).toLocaleDateString()}</p>
        {/if}
      </div>
    </div>

    <!-- Raw JSON for debugging (optional) -->
    <details>
      <summary>Raw User Object (for debugging)</summary>
      <pre>{JSON.stringify($user, null, 2)}</pre>
    </details>
  </div>
{/if}

<style>
  .profile-container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 1rem;
  }

  .profile-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    background-color: #f9f9f9;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
  }

  .profile-picture {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
  }

  .profile-info {
    flex: 1;
  }

  .profile-info p {
    margin: 0.5rem 0;
  }

  h2 {
    color: #333;
    margin-bottom: 1rem;
  }

  details {
    margin-top: 1rem;
  }

  pre {
    background-color: #f4f4f4;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 0.9em;
  }
</style>
```

### ✅ Checkpoint

Run your application and verify that:

- When you are logged in, you can see your user profile information displayed
- Your profile picture, name, and email are shown correctly
- When you are logged out, the profile information is hidden

## 7. Call a Protected API (Optional)

If you want to call a protected API from your Svelte application, you'll need to get an access token and include it in your API requests. Here's how you can do that:

Create a new file called `api.js` in your `src/lib` directory:

```javascript
// src/lib/api.js
import { get } from 'svelte/store';
import { auth0Client, authError } from './auth.js';

export async function getAccessToken(options = {}) {
  try {
    const client = get(auth0Client);
    if (!client) {
      throw new Error('Auth0 client not initialized');
    }

    const token = await client.getTokenSilently({
      authorizationParams: {
        audience: 'YOUR_API_IDENTIFIER', // Replace with your API identifier
        scope: 'openid profile email read:posts', // Add your required scopes
      },
      ...options
    });

    return token;
  } catch (error) {
    authError.set(error);
    
    // If login is required, redirect to login
    if (error.error === 'login_required') {
      const client = get(auth0Client);
      if (client) {
        await client.loginWithRedirect();
      }
    }
    
    throw error;
  }
}

export async function callProtectedAPI(endpoint, options = {}) {
  try {
    const token = await getAccessToken();
    
    const response = await fetch(endpoint, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`API call failed: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API call error:', error);
    throw error;
  }
}
```

You can then use this in your Svelte components:

```svelte
<script>
  import { callProtectedAPI } from './lib/api.js';

  async function fetchUserData() {
    try {
      const data = await callProtectedAPI('/api/user-data');
      console.log('Protected data:', data);
    } catch (error) {
      console.error('Failed to fetch protected data:', error);
    }
  }
</script>
```

## 8. Handle Common Errors

Here are some common error scenarios and how to handle them in your Svelte application:

```javascript
// src/lib/errorHandler.js
import { authError } from './auth.js';

export function handleAuthError(error) {
  console.error('Auth error:', error);
  
  switch (error.error) {
    case 'login_required':
      // User needs to log in
      authError.set('Please log in to continue');
      break;
    case 'consent_required':
      // User needs to give consent
      authError.set('Additional permissions required');
      break;
    case 'popup_timeout':
      // Popup login timed out
      authError.set('Login timed out. Please try again.');
      break;
    case 'popup_cancelled':
      // User cancelled popup
      authError.set('Login was cancelled');
      break;
    default:
      authError.set('An authentication error occurred');
  }
}
```

Add error display to your main `App.svelte`:

```svelte
<!-- Add this to your App.svelte -->
<script>
  import { authError } from './lib/auth.js';
  
  // Clear error after 5 seconds
  $: if ($authError) {
    setTimeout(() => {
      authError.set(null);
    }, 5000);
  }
</script>

{#if $authError}
  <div class="error-banner">
    <p>⚠️ {$authError.message || $authError}</p>
  </div>
{/if}

<style>
  .error-banner {
    background-color: #f8d7da;
    color: #721c24;
    padding: 1rem;
    margin: 1rem 0;
    border: 1px solid #f5c6cb;
    border-radius: 4px;
  }
</style>
```

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

*Did this help you get started with Auth0 in your Svelte application? We'd love to hear your feedback in the [Auth0 Community](https://community.auth0.com/)!*
