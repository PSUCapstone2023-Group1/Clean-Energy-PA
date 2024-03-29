from .test_green_energy_base import GreenEnergySearchBaseTest
from web_parser.tests import ratesearch_test_data
import json
import copy

class TestViews_Possible_Selections(GreenEnergySearchBaseTest):

    def setUp(self):
        super().setUp()

    def test_get_possible_selections(self):
        """Test the get endpoint for possible selections"""

        #Login the user
        self.client.force_login(self.user)
        self.user.is_active=True
        self.user.save()
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user.is_active)

        response = self.client.get(self.possible_selections_url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertTrue("offers" in data)
        self.assertTrue("last_updated" in data)
        self.assertEqual(len(data["offers"]), 2)
    
    def test_post_possible_selections(self):
        """Test the post endpoint for possible selections"""

        orig_sel_count = len(self.user_preferences.get_possible_selections())

        #Login the user
        self.client.force_login(self.user)
        self.user.is_active=True
        self.user.save()
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user.is_active)
        
        #Create a "unique test entry to post"
        new_entry = copy.deepcopy(ratesearch_test_data.expected_example[0])
        new_entry["id"]=3

        response = self.client.post(self.possible_selections_url, json.dumps(new_entry), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.user_preferences.refresh_from_db()
        self.assertEqual(len(self.user_preferences.get_possible_selections()), orig_sel_count+1)

    def test_post_possible_selections_no_auth(self):
        """Test the post endpoint for possible selections not authenticated"""
        response = self.client.post(self.possible_selections_url, json.dumps(ratesearch_test_data.expected_example[0]), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_post_possible_selections_no_active(self):
        """Test the post endpoint for possible selections not authenticated"""
        
        self.client.force_login(self.user)
        self.user.save()
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

        response = self.client.post(self.possible_selections_url, json.dumps(ratesearch_test_data.expected_example[0]), content_type='application/json')
        self.assertEqual(response.status_code, 403)
    
    def test_delete_possible_selections(self):
        """Test the post endpoint for possible selections"""

        #Login the user
        self.client.force_login(self.user)
        self.user.is_active=True
        self.user.save()
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user.is_active)
        
        response = self.client.delete(self.possible_selections_url)
        self.assertEqual(response.status_code, 200)
        self.user_preferences.refresh_from_db()
        self.assertEqual(len(self.user_preferences.get_possible_selections()), 0)

    def test_delete_current_selection(self):
        """Test the post endpoint for possible selections"""

        #Login the user
        self.client.force_login(self.user)
        self.user.is_active=True
        self.user.save()
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user.is_active)
        
        response = self.client.delete(self.current_selection_url)
        self.assertEqual(response.status_code, 200)
        self.user_preferences.refresh_from_db()
        self.assertFalse(self.user_preferences.has_selected_offer())
    
    def test_put_current_selection(self):
        """Test the post endpoint for possible selections"""

        #Login the user
        self.client.force_login(self.user)
        self.user.is_active=True
        self.user.save()
        self.assertTrue(self.user.is_authenticated)
        self.assertTrue(self.user.is_active)
        
        #Create a "unique test entry to post"
        new_entry = copy.deepcopy(ratesearch_test_data.expected_example[0])
        new_id = 3
        new_entry["id"]=new_id

        response = self.client.put(self.current_selection_url, json.dumps(new_entry), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.user_preferences.refresh_from_db()
        self.assertEqual(str(self.user_preferences.get_selected_offer().id), str(new_id))