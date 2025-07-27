#!/usr/bin/env python3
"""Unit tests for Quickstart Prompt Generator CLI."""

import os
import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.cli import SessionManager, cli
from src.prompts import PromptGenerator
from click.testing import CliRunner


class TestSessionManager(unittest.TestCase):
    """Test SessionManager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.original_cwd)
        if os.path.exists(os.path.join(self.temp_dir, '.qpg_session.json')):
            os.remove(os.path.join(self.temp_dir, '.qpg_session.json'))
        os.rmdir(self.temp_dir)
    
    def test_session_initialization(self):
        """Test SessionManager initialization with default values."""
        session = SessionManager()
        expected_keys = ['sdk_name', 'sdk_language', 'sdk_repository', 'reference_links', 'target_framework']
        
        for key in expected_keys:
            self.assertIn(key, session.session_data)
        
        self.assertEqual(session.session_data['sdk_name'], '')
        self.assertEqual(session.session_data['reference_links'], [])
    
    def test_session_save_and_load(self):
        """Test session persistence."""
        session = SessionManager()
        test_data = {
            'sdk_name': 'test-sdk',
            'sdk_language': 'Python',
            'target_framework': 'Django'
        }
        
        session.update_data(**test_data)
        
        # Create new session to test loading
        new_session = SessionManager()
        
        for key, value in test_data.items():
            self.assertEqual(new_session.session_data[key], value)
    
    def test_session_update_data(self):
        """Test session data updates."""
        session = SessionManager()
        session.update_data(sdk_name='updated-sdk', sdk_language='JavaScript')
        
        self.assertEqual(session.session_data['sdk_name'], 'updated-sdk')
        self.assertEqual(session.session_data['sdk_language'], 'JavaScript')
    
    def test_get_data_returns_copy(self):
        """Test that get_data returns a copy, not reference."""
        session = SessionManager()
        data = session.get_data()
        data['sdk_name'] = 'modified'
        
        self.assertNotEqual(session.session_data['sdk_name'], 'modified')


class TestPromptGenerator(unittest.TestCase):
    """Test PromptGenerator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = PromptGenerator()
        self.sample_data = {
            'sdk_name': 'test-sdk',
            'sdk_language': 'Python',
            'sdk_repository': 'https://github.com/test/test-sdk',
            'reference_links': ['https://example.com/docs'],
            'target_framework': 'Django'
        }
    
    def test_template_initialization(self):
        """Test that all templates are loaded."""
        expected_templates = ['sdk_analysis', 'style_extraction', 'synthesis']
        
        for template_name in expected_templates:
            self.assertIn(template_name, self.generator.templates)
            self.assertIsInstance(self.generator.templates[template_name], str)
            self.assertGreater(len(self.generator.templates[template_name]), 0)
    
    def test_sdk_analysis_prompt_generation(self):
        """Test SDK analysis prompt generation."""
        prompt = self.generator.generate_sdk_analysis_prompt(self.sample_data)
        
        self.assertIsInstance(prompt, str)
        self.assertIn('test-sdk', prompt)
        self.assertIn('Python', prompt)
        self.assertIn('Django', prompt)
        self.assertIn('SDK Deep Analysis Request', prompt)
    
    def test_style_extraction_prompt_generation(self):
        """Test style extraction prompt generation."""
        prompt = self.generator.generate_style_extraction_prompt(self.sample_data)
        
        self.assertIsInstance(prompt, str)
        self.assertIn('test-sdk', prompt)
        self.assertIn('Django', prompt)
        self.assertIn('https://example.com/docs', prompt)
        self.assertIn('Reference Documentation Style Analysis', prompt)
    
    def test_synthesis_prompt_generation(self):
        """Test synthesis prompt generation."""
        prompt = self.generator.generate_synthesis_prompt(self.sample_data)
        
        self.assertIsInstance(prompt, str)
        self.assertIn('test-sdk', prompt)
        self.assertIn('Python', prompt)
        self.assertIn('Django', prompt)
        self.assertIn('Quickstart Documentation Generation Request', prompt)
    
    def test_prompt_with_missing_optional_fields(self):
        """Test prompt generation with missing optional fields."""
        minimal_data = {
            'sdk_name': 'minimal-sdk',
            'sdk_language': 'Java',
            'sdk_repository': '',
            'reference_links': [],
            'target_framework': 'Spring Boot'
        }
        
        # Should not raise exceptions
        sdk_prompt = self.generator.generate_sdk_analysis_prompt(minimal_data)
        style_prompt = self.generator.generate_style_extraction_prompt(minimal_data)
        synthesis_prompt = self.generator.generate_synthesis_prompt(minimal_data)
        
        self.assertIn('minimal-sdk', sdk_prompt)
        self.assertIn('Spring Boot', style_prompt)
        self.assertIn('Java', synthesis_prompt)
    
    def test_custom_template_addition(self):
        """Test adding custom templates."""
        custom_template = "Custom template for {{ sdk_name }}"
        self.generator.add_custom_template('custom', custom_template)
        
        self.assertIn('custom', self.generator.templates)
        self.assertEqual(self.generator.templates['custom'], custom_template)
    
    def test_template_update(self):
        """Test updating existing templates."""
        original_template = self.generator.templates['sdk_analysis']
        new_template = "Updated template"
        
        self.generator.update_template('sdk_analysis', new_template)
        self.assertEqual(self.generator.templates['sdk_analysis'], new_template)
        self.assertNotEqual(self.generator.templates['sdk_analysis'], original_template)
    
    def test_template_update_nonexistent(self):
        """Test updating non-existent template raises error."""
        with self.assertRaises(KeyError):
            self.generator.update_template('nonexistent', 'new template')
    
    def test_list_templates(self):
        """Test listing available templates."""
        templates = self.generator.list_templates()
        expected = ['sdk_analysis', 'style_extraction', 'synthesis']
        
        for template_name in expected:
            self.assertIn(template_name, templates)
    
    def test_get_template_info(self):
        """Test getting template information."""
        info = self.generator.get_template_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('sdk_analysis', info)
        self.assertIn('style_extraction', info)
        self.assertIn('synthesis', info)


class TestCLICommands(unittest.TestCase):
    """Test CLI command functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures."""
        session_file = os.path.join(self.temp_dir, '.qpg_session.json')
        if os.path.exists(session_file):
            os.remove(session_file)
        os.rmdir(self.temp_dir)
    
    def test_cli_version(self):
        """Test CLI version command."""
        result = self.runner.invoke(cli, ['--version'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('1.0.0', result.output)
    
    def test_cli_help(self):
        """Test CLI help command."""
        result = self.runner.invoke(cli, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Quickstart Prompt Generator', result.output)
        self.assertIn('init', result.output)
        self.assertIn('generate', result.output)
    
    @patch('src.cli.click.prompt')
    def test_init_command(self, mock_prompt):
        """Test init command with mocked input."""
        mock_prompt.side_effect = [
            'test-sdk',           # SDK name
            'Python',             # SDK language  
            'https://test.com',   # SDK repository
            '',                   # Empty reference (end input)
            'Django'              # Target framework
        ]
        
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['init'])
            
            self.assertEqual(result.exit_code, 0)
            self.assertIn('Session initialized successfully', result.output)
            
            # Check session file was created
            self.assertTrue(os.path.exists('.qpg_session.json'))
            
            # Check session data
            with open('.qpg_session.json', 'r') as f:
                session_data = json.load(f)
            
            self.assertEqual(session_data['sdk_name'], 'test-sdk')
            self.assertEqual(session_data['sdk_language'], 'Python')
            self.assertEqual(session_data['target_framework'], 'Django')
    
    def test_status_command_no_session(self):
        """Test status command with no active session."""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['status'])
            
            self.assertEqual(result.exit_code, 0)
            self.assertIn('No active session found', result.output)
    
    def test_status_command_with_session(self):
        """Test status command with active session."""
        session_data = {
            'sdk_name': 'test-sdk',
            'sdk_language': 'Python',
            'sdk_repository': '',
            'reference_links': ['https://example.com'],
            'target_framework': 'Django'
        }
        
        with self.runner.isolated_filesystem():
            with open('.qpg_session.json', 'w') as f:
                json.dump(session_data, f)
            
            result = self.runner.invoke(cli, ['status'])
            
            self.assertEqual(result.exit_code, 0)
            self.assertIn('test-sdk', result.output)
            self.assertIn('Python', result.output)
            self.assertIn('Django', result.output)
    
    def test_reset_command(self):
        """Test reset command."""
        with self.runner.isolated_filesystem():
            # Create a session file
            with open('.qpg_session.json', 'w') as f:
                json.dump({'sdk_name': 'test'}, f)
            
            result = self.runner.invoke(cli, ['reset'])
            
            self.assertEqual(result.exit_code, 0)
            self.assertIn('Session reset successfully', result.output)
            self.assertFalse(os.path.exists('.qpg_session.json'))
    
    def test_generate_command_no_session(self):
        """Test generate command with missing session data."""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['generate'])
            
            self.assertEqual(result.exit_code, 0)
            self.assertIn('Missing required information', result.output)
    
    def test_generate_command_with_session(self):
        """Test generate command with complete session."""
        session_data = {
            'sdk_name': 'test-sdk',
            'sdk_language': 'Python',
            'sdk_repository': 'https://test.com',
            'reference_links': ['https://example.com'],
            'target_framework': 'Django'
        }
        
        with self.runner.isolated_filesystem():
            with open('.qpg_session.json', 'w') as f:
                json.dump(session_data, f)
            
            result = self.runner.invoke(cli, ['generate'])
            
            self.assertEqual(result.exit_code, 0)
            self.assertIn('Generating prompts', result.output)
            self.assertIn('Stage 1: SDK Deep Analysis', result.output)
            self.assertIn('Stage 2: Reference Style Extraction', result.output)
            self.assertIn('Stage 3: Quickstart Synthesis', result.output)
    
    def test_generate_command_markdown_output(self):
        """Test generate command with markdown output to file."""
        session_data = {
            'sdk_name': 'test-sdk',
            'sdk_language': 'Python',
            'sdk_repository': '',
            'reference_links': [],
            'target_framework': 'Django'
        }
        
        with self.runner.isolated_filesystem():
            with open('.qpg_session.json', 'w') as f:
                json.dump(session_data, f)
            
            result = self.runner.invoke(cli, ['generate', '--format', 'markdown', '--output', 'test-prompts.md'])
            
            self.assertEqual(result.exit_code, 0)
            self.assertIn('Prompts saved to test-prompts.md', result.output)
            self.assertTrue(os.path.exists('test-prompts.md'))
            
            # Check file content
            with open('test-prompts.md', 'r') as f:
                content = f.read()
            
            self.assertIn('# Quickstart Prompt Generator Output', content)
            self.assertIn('## Stage 1: SDK Deep Analysis Prompt', content)
            self.assertIn('test-sdk', content)


class TestIntegration(unittest.TestCase):
    """Integration tests for full workflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    @patch('src.cli.click.prompt')
    @patch('src.cli.click.pause')
    def test_full_workflow(self, mock_pause, mock_prompt):
        """Test complete init -> generate workflow."""
        # Mock user inputs for init
        mock_prompt.side_effect = [
            'auth0-python',                           # SDK name
            'Python',                                 # SDK language
            'https://github.com/auth0/auth0-python', # SDK repository
            'https://auth0.com/docs/quickstart',     # Reference 1
            '',                                       # End references
            'Flask'                                   # Target framework
        ]
        
        # Mock pause for interactive display
        mock_pause.return_value = None
        
        with self.runner.isolated_filesystem():
            # Test init command
            init_result = self.runner.invoke(cli, ['init'])
            self.assertEqual(init_result.exit_code, 0)
            self.assertIn('Session initialized successfully', init_result.output)
            
            # Test status command
            status_result = self.runner.invoke(cli, ['status'])
            self.assertEqual(status_result.exit_code, 0)
            self.assertIn('auth0-python', status_result.output)
            
            # Test generate command
            generate_result = self.runner.invoke(cli, ['generate'])
            self.assertEqual(generate_result.exit_code, 0)
            self.assertIn('SDK Deep Analysis', generate_result.output)
            
            # Test generate with file output
            file_result = self.runner.invoke(cli, ['generate', '-f', 'text', '-o', 'prompts.txt'])
            self.assertEqual(file_result.exit_code, 0)
            self.assertTrue(os.path.exists('prompts.txt'))


if __name__ == '__main__':
    # Run tests with detailed output
    unittest.main(verbosity=2)
