# nytimes-top-stories

`nytimes-top-stories` is a simple Python wrapper for New York Times' Top Stories API.

Compatible with Python 2.7 and 3+.

## Dependencies

`nytimes-top-stories` requires the `requests` package.

## Installation

### Pip
```pip install nytimes-top-stories```

### Clone repository

- ```git clone git@github.com:kashiish/nytimes-top-stories.git```
- ```cd``` into your ```nytimes-top-stories``` directory
- ```python setup.py install```

## Usage

Register for a Top Stories API key at https://developer.nytimes.com/signup.

```python
from topstories import TopStoriesAPI

api = TopStoriesAPI(<SECRET_API_KEY>)

```
The ```get_stories``` method takes one required argument and two optional arguments.
Checkout the [API documentation](https://developer.nytimes.com/top_stories_v2.json#) to see what data
is returned from the API.


```python def
def get_stories(self, section, format_type="json", return_json_string=False):
      """

      Gets a list of current top articles and associated images in the
      specified section and in the specified format.

      params:
          section: (string) the section the articles appears in
          format: (string) json or jsonp, default is json
          return_json_string: (boolean) if True, return value will be JSON string instead of a python list,
                              default is False
      return:
          format_type=json: A list of articles (articles are python dicts) is returned.
                            If return_json_string, string is returned.
          format_type=jsonp: API returns a callback function (string) in the format
                            "{section}TopStoriesCallback({data})".
                            {data} is an object, not an array, and it is not parsed/decoded.
      """
```

```python def

stories = api.get_stories("politics") # list of story dicts
stories_string = api.get_stories("home", return_json_string=True) # json string
stories_jsonp = api.get_stories("work", format_type="jsonp") # (string) callback function with data input

```

In addition, there are two more public methods:

```python def
#returns a list of valid sections
>>> api.get_sections_list()
>>> ["home", "opinion","world","national","politics","upshot","nyregion","business",
    "technology","science","health","sports","arts","books","theater","sundayreview",
    "fashion","tmagazine","food","travel","magazine","realestate","automobiles",
    "obituaries","insider"]

```

```python def

# writes a list of stories to a json file
# input a path to file and list of stories
>>> api.write_to_json_file("example.json", stories)

```

## Testing

`pytest` and `mock` are used for testing this package.

**Pytest 3.3.0+ does not support Python 3.3.**

```python setup.py pytest```

## Other

Please report any bugs you may find or any suggestions you may have.

Thanks!
