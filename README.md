# Closet Statistics

This is a simple application used to help track the visits to the Compassion Closet, regardless of the location. At its core, this is a web site that is hosted at heroku and present on the Internet at https://closet-stats.herokuapp.com.

## Magic Switches

The application is designed to work as seamlessly as possible (sensible defaults). However, there are times when you need to add a little configuration and the app also supports those scenarios.

### Automatic setting of the location

The application defaults to showing Knoxville (alphabetic) as the location. This is fine for the Knoxville location, but it is a pain if the Oak Ridge (or other locations) constantly have to switch it. Therefore, there is a URL parameter `loc` that, if set to `2`, will cause the application to default to Oak Ridge. Therefore, the devices used at that location should have the memorized/bookmarked URL set to https://closet-stats.herokuapp.com?loc=2. A Mapping for avalid `loc` (location) values is as follows:

| value | location |
|:---:|:------------|
| 1 | Knoxville |
| 2 | Oak Ridge |
| 3 | North Knox |
| 4 | Seymour |
| 5 | Campbell County |

### Make the Timestamp Visible

The timestamp of the entry is calculated and sent by default with each entry. The setting is slighly cryptic and not the most user-friendly of formats. However, there are times where you are working with old data and need to enter it, so you want to show the timestamp control so that you can override the auto-calculated value. This can be done by setting the `ts=1` querystring parameter.


## Publishing Notes

```bash
heroku --version

# uses browser to do some magic
heroku login 

# upgrade
git push -u heroku master

# run it locally
heroku local -p 8000

# web: gunicorn app.main:app --log-level=debug

```