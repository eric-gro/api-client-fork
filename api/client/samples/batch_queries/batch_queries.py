import os
# change this import so it doesn't import from groclient but rather from the relative directory
# from groclient import GroClient
# you need to add /api-client to the PYTHONPATH envvar
from groclient.client import GroClient

def main():
    # set up the Batch Client, same as normal Client
    """ API Config """
    API_HOST = 'api.gro-intelligence.com'
    ACCESS_TOKEN = os.environ['GROAPI_TOKEN']
    PROXY_HOST = '0.0.0.0'
    PROXY_PORT = 8080
    api_client = GroClient(API_HOST, ACCESS_TOKEN, PROXY_HOST, PROXY_PORT)

    # specify everything except region_id
    selection = {
        'metric_id': 860032,
        'item_id': 274,
        'source_id': 25,
        'frequency_id': 9,
        'start_date': '1998-01-01T00:00:00.000Z',
        'end_date': '1998-01-01T00:00:00.000Z'
    }

    # make a list of this query for every county in Mississippi
    mississippi_county_ids = [region["id"] for region in api_client.get_descendant_regions(13075, 5)]

    selections = []
    for region_id in mississippi_county_ids:
        selection_temp = dict(selection)
        selection_temp["region_id"] = region_id
        selections.append(selection_temp)

    # make the request in a batch, asynchronous way
    output = api_client.batch_async_get_data_points(selections)

    # the output data is in the same order as the input queries. 
    for county_id, data in zip(mississippi_county_ids, output):
        if len(data) > 0: # some counties are missing data
            print("county_idx=%i produced %.0f tonnes of corn in 1998" % (county_id, data[0]["value"]))
        else:
            print("county_idx=%i has no data for 1998" % county_id)

if __name__ == "__main__":
        main()
