response_dict = {400: 'Bad request',
                 401: 'Unauthorized',
                 403: 'Forbidden',
                 404: 'Data not found',
                 405: 'Method not allowed',
                 415: 'Unsupported media type',
                 429: 'Rate limit exceeded, another try in {time}s',
                 500: 'Internal server error',
                 502: 'Bad gateway',
                 503: 'Service unavailable',
                 504: 'Gateway timeout'
                 }

# sample_data = {
#   "data": [
#     {
#       "title": "string",
#       "salary_from": null,
#       "salary_to": null,
#       "rate": "monthly",
#       "is_remote": false,
#       "remote_range": 100,
#       "is_gross": false,
#       "description": "string",
#       "recruitment": "string",
#       "email": "user@example.com",
#       "currency": "PLN",
#       "plan": "plus",
#       "seniority": "student",
#       "employment": "employment",
#       "locations": [
#         {
#           "city": "string",
#           "street": "string",
#           "street_number": "string",
#           "country": "string",
#           "latitude": 0,
#           "longitude": 0
#         }
#       ],
#       "tags": [
#         {
#           "name": "string",
#           "priority": 1
#         }
#       ],
#       "firm": {
#         "name": "string",
#         "is_agency": false,
#         "website": "string",
#         "logo": "string",
#         "description": "string",
#         "youtube_url": "string",
#         "latitude": 0,
#         "longitude": 0,
#         "street": "string",
#         "street_number": "string",
#         "city": "string",
#         "country": "string",
#         "postcode": "string"
#       }
#     }
#   ],
#   "meta": {
#     "current_page": 1,
#     "from": 1,
#     "last_page": 1,
#     "path": "string",
#     "per_page": 0,
#     "to": 1,
#     "total": 1
#   }
# }