import pytest
from requests import HTTPError
from mock import Mock, patch, mock_open
from topstories import top_stories

@pytest.fixture
def api():
	API_KEY = "test"
	return top_stories.TopStoriesAPI(API_KEY);

@pytest.fixture
def response_text():
	return """{"status":"OK", "section":"science", "results":[{"section":"Science", "title":"test_title"}]}"""

@pytest.fixture
def json_return_value():
	return {"status": "OK", "section":"science", "results": [{"section": "Science", "title": "test_title"}]}


@patch("requests.get")
def test_get_stories_json(mock_get, response_text, json_return_value, api):
	"""
	Tests an API call to get the current top stories from the NYTimes in json format.
	"""
	mock_get.return_value = Mock(text=response_text)
	mock_get.return_value.json.return_value = json_return_value

	#json is the default format_type
	stories = api.get_stories("science")

	#use the first item to test type and keys
	first_item = stories[0]

	assert isinstance(stories, list)
	assert isinstance(first_item, dict)


@patch("requests.get")
def test_get_stories_return_json_string(mock_get, response_text, json_return_value, api):

	mock_get.return_value = Mock(text=response_text)
	mock_get.return_value.json.return_value = json_return_value

	stories_json_string = api.get_stories("science", return_json_string = True)

	try:
		assert isinstance(stories_json_string, basestring)
	except NameError:
		assert isinstance(stories_json_string, str)

@patch("requests.get")
def test_get_stories_jsonp(mock_get, api):
	"""
	Tests an API call to get the current top stories from the NYTimes in jsonp format.
	"""

	response_text = """homeTopStoriesCallback({"status": "OK", "section": "home", "results": [{"section": "home", "title": "test_title"}]})"""

	mock_get.return_value = Mock(text=response_text)

	javascript_func = api.get_stories("home", "jsonp")

	try:
		assert isinstance(javascript_func, basestring)
	except NameError:
		assert isinstance(javascript_func, str)

	assert "homeTopStoriesCallback" in javascript_func


@patch("requests.get")
def test_get_stories_http_error(mock_get, api):

	mock_get.return_value = Mock(status_code=404)
	mock_get.return_value.raise_for_status.side_effect = HTTPError

	with pytest.raises(Exception):
		api.get_stories("books")


def test_invalid_section(api):
	"""
	Tests whether or not an invalid section argument in get_top_stories raises an error.
	"""

	with pytest.raises(top_stories.InvalidSectionType):
		api.get_stories("work")



def test_invalid_format(api):
	"""
	Tests whether or not an invalid format argument in get_top_stories raises an error.
	"""
	with pytest.raises(top_stories.InvalidFormatType):
		api.get_stories("home", "xml")


def test_api_key_error(api):
	"""
	Tests if missing API key raises error.
	"""
	with pytest.raises(top_stories.APIKeyError):
		missingAPI = top_stories.TopStoriesAPI()

@patch("requests.get")
def test_invalid_authentication(mock_get, api):
	"""
	Tests if invalid API key raises error.
	"""

	error_message = """{"message": "Invalid authentication credentials"}"""
	mock_get.return_value = Mock(text=error_message, status_code=403)
	mock_get.return_value.raise_for_status.side_effect = HTTPError

	with pytest.raises(top_stories.InvalidAuthentication):
		api.get_stories("opinion")


@pytest.fixture
def test_assertions_for_json_file(m_dump, m_open, api):
	stories_list = [{"section": "Politics", "title": "test_title"}]
	api.write_to_json_file("test.json", stories_list)
	m_open.assert_called_once_with("test.json", "w+")
	m_dump.assert_called_with(stories_list, m_open.return_value.__enter__.return_value)


def test_write_to_file(api):
	"""
	Tests function that writes API call data to a JSON file.
	"""
	try:
		with patch("__builtin__.open", new_callable=mock_open()) as m_open:
			with patch("json.dump") as m_dump:
				test_assertions_for_json_file(m_dump, m_open, api)
	except ImportError:
		with patch("builtins.open", new_callable=mock_open()) as m_open:
			with patch("json.dump") as m_dump:
				test_assertions_for_json_file(m_dump, m_open, api)
