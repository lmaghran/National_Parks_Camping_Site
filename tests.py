import unittest
from server import app
from model import Campsite, Recreation_area, connect_to_db, db
from server_functions import rec_area_list, random_images, get_np_info, get_nps_photos, get_campsites, get_avail_dictionary, return_cg_lat_long, generate_availibility_dictionary, generate_campsite_dictionary


def example_data():
    c1 = Campsite(
    facility_id= 247591,
    parent_rec_area_id=2881,
    campsite_name= "Mora Campground",
    campsite_lat= 0.0,
    campsite_long= 0.0,
    is_reservable = True,
    campsite_type = "Campground",
    campsite_description= "<h2>Overview</h2>\n<p>Nestled in a coastal forest, Mora Campground"
        )

    c2 = Campsite(
    facility_id=232452,
    parent_rec_area_id=2991,
    campsite_name= "CRANE FLAT",
    campsite_lat= 37.7638889,
    campsite_long= -119.8444444,
    is_reservable = True,
    campsite_type = "Campground",
    campsite_description= "<h2>Overview</h2>\nCrane Flat Campground is located in breathtaking Yosemite National Park in Central California's rugged Sierra Nevada Mountain Range.The site"
        )

    f1 = Recreation_area(
        rec_area_id =2881,
        rec_id_name = "OLYM",
        rec_name= "Olympic National Park",
        rec_area_des="With its incredible range of precipitation and elevation, diversity is the hallmark of Olympic National Park. Encompassing nearly a million acres, the park protects a vast wilderness, thousands of years"
        )

    f2 = Recreation_area(
        rec_area_id =2991,
        rec_id_name = "YOSE",
        rec_name= "Yosemite National Park",
        rec_area_des= "Not just a great valley, but a shrine to human foresight, the strength of granite,"

        )

    f3 = Recreation_area(
        rec_area_id =14520,
        rec_id_name = "CAMO",
        rec_name= "Castle Mountains National Monument",
        rec_area_des= "Castle Mountains represents some of the most unique elements..."
        )



    db.session.add_all([f1, f2, c1, c2])
    db.session.commit()


class CampingTests(unittest.TestCase):
    """Tests for camping site."""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'KEY'
        self.client = app.test_client()
        connect_to_db(app, "postgresql:///testdb")
        # Create tables and add sample data
        db.create_all()
        example_data()

    def test_rec_area_list(self):
        self.assertEqual(len(rec_area_list()), 2)

    def test_random_images(self):
        rec_areas=rec_area_list()
        self.assertEqual(len(random_images(rec_areas)), 7)

    def test_get_np_info(self):
        selected_area= "Yosemite National Park"
        self.assertTrue(len(get_np_info(selected_area))>1)

    def test_get_nps_photos(self):
        nps_code= "CAMO"
        self.assertListEqual(get_nps_photos(nps_code), [{'credit': 'NPS.Photo', 'altText': 'Red rocks frame a stand of Joshua trees and sage brush.', 'title': 'Red Rocks Outcropping', 'id': '4474', 'caption': 'Red rocks frame a stand of Joshua trees and sage brush in the desert floor..', 'url': 'https://www.nps.gov/common/uploads/structured_data/3C87A219-1DD8-B71B-0BF28720E6A4AC75.jpg'}])


    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"Tentative", result.data)

    def test_no_selection_yet(self):
        result = self.client.get("/")
        self.assertNotIn(b"Enter a check-in date:", result.data)

    def test_get_avail_dictionary(self):
        camp_id= 247591
        start_date='2020-03-02'
        end_date='2020-03-03'
        self.assertTrue(get_avail_dictionary(camp_id, start_date, end_date))

    def test_get_campsites(self):
        selected_area= "Yosemite National Park"
        self.assertTrue(get_campsites(selected_area))

    def test_generate_campsite_dictionary(self):
        selected_campsites= get_campsites("Yosemite National Park")
        start_date='2020-03-02'
        end_date='2020-03-03'
        self.assertTrue(generate_campsite_dictionary(selected_campsites, start_date, end_date))

    def test_return_cg_lat_long(self):
        self.assertTrue(return_cg_lat_long())

    def test_generate_availibility_dictionary(self):
        with app.test_request_context():
            self.assertIn("availibility", generate_availibility_dictionary()['mapping_list'][0].keys())

    def test_selected(self):
        result = self.client.get("/np_selected",
                                  query_string= {'rec_area': 'Olympic National Park'},
                                  follow_redirects=True)

    def test_selected(self):
        result = self.client.get("/np_selected",
                                  query_string= {'rec_area': 'Olympic National Park'},
                                  follow_redirects=True)

    def tearDown(self):

        db.session.close()
        db.drop_all()

class CampsiteTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    # def test_games(self):
    #     """Test departments page."""

    #     result = self.client.get("/games")
    #     self.assertIn(b"Power Grid", result.data)


if __name__ == "__main__":
    unittest.main()
