response_dict = {400: 'błędny request',
                 401: 'błędny klucz',
                 403: 'brak dostępu',
                 404: 'brak danych',
                 405: 'zabroniona metoda',
                 415: 'nieobsługiwany typ mediów',
                 429: 'przekroczony limit requestów, próba ponownego połączenia za {time}s',
                 500: 'server is down',
                 502: 'błąd gatewaa',
                 503: 'serwis niedostępny',
                 504: 'przekroczony czas gatewaya'
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