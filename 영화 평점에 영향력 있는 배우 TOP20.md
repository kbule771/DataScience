```python
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import requests
# data visualization
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session
```

```
/kaggle/input/tmdb-movie-metadata/tmdb_5000_movies.csv
/kaggle/input/tmdb-movie-metadata/tmdb_5000_credits.csv
```

```python
credits = pd.read_csv('../input/tmdb-movie-metadata/tmdb_5000_credits.csv')# 제작자 관련 데이터 저장하기
movies = pd.read_csv('../input/tmdb-movie-metadata/tmdb_5000_movies.csv')# 영화 관련 데이터 저장하기

movie_credit = pd.merge(credits, movies)# 데이터 합치기
```

```python

movie_credit = movie_credit.sort_values(by='release_date', ascending=True) # 날짜순으로 데이터 정렬
# print(type(int(movie_credit['release_date'][0][:1]))) # 맨앞자리 년도 확인하기
# print(movie_credit['release_date'][:1])
movie_credit[movie_credit['release_date'] >= '2000-01-01'] # 2000년 이후 날짜 만 필터하기
```

|      | movie_id |                     title |                                              cast |                                              crew |   budget |                                            genres |                                         homepage |     id |                                          keywords | original_language |  ... |                              production_companies |                              production_countries | release_date |  revenue | runtime |                               spoken_languages |   status |                                           tagline | vote_average | vote_count |
| ---: | -------: | ------------------------: | ------------------------------------------------: | ------------------------------------------------: | -------: | ------------------------------------------------: | -----------------------------------------------: | -----: | ------------------------------------------------: | ----------------: | ---: | ------------------------------------------------: | ------------------------------------------------: | -----------: | -------: | ------: | ---------------------------------------------: | -------: | ------------------------------------------------: | -----------: | ---------- |
| 2778 |    48217 | The Widow of Saint-Pierre | [{"cast_id": 1, "character": "Jean, le capitai... | [{"credit_id": "52fe475ac3a36847f8130f4d", "de... |        0 | [{"id": 10749, "name": "Romance"}, {"id": 18, ... |                                              NaN |  48217 | [{"id": 254, "name": "france"}, {"id": 2041, "... |                en |  ... | [{"name": "Cin\u00e9maginaire Inc.", "id": 280... | [{"iso_3166_1": "FR", "name": "France"}, {"iso... |   2000-01-01 |        0 |   112.0 | [{"iso_639_1": "fr", "name": "Fran\u00e7ais"}] | Released |                                               NaN |          6.7 | 11         |
| 3146 |    10471 |               Next Friday | [{"cast_id": 1, "character": "Craig Jones", "c... | [{"credit_id": "52fe43769251416c75011535", "de... | 11000000 |                    [{"id": 35, "name": "Comedy"}] |                                              NaN |  10471 | [{"id": 378, "name": "prison"}, {"id": 1522, "... |                en |  ... |           [{"name": "New Line Cinema", "id": 12}] | [{"iso_3166_1": "US", "name": "United States o... |   2000-01-12 | 59827328 |    98.0 |       [{"iso_639_1": "en", "name": "English"}] | Released |              The suburbs make the hood look good. |          6.4 | 135        |
|  775 |    10384 |                 Supernova | [{"cast_id": 6, "character": "Nick Vanzant", "... | [{"credit_id": "52fe43639251416c7500e78f", "de... | 90000000 | [{"id": 27, "name": "Horror"}, {"id": 878, "na... |                                              NaN |  10384 | [{"id": 577, "name": "black people"}, {"id": 1... |                en |  ... | [{"name": "United Artists", "id": 60}, {"name"... | [{"iso_3166_1": "CH", "name": "Switzerland"}, ... |   2000-01-14 | 14828081 |    91.0 |       [{"iso_639_1": "en", "name": "English"}] | Released | In the farthest reaches of space, something ha... |          4.9 | 109        |
| 3349 |    17908 |               My Dog Skip | [{"cast_id": 1, "character": "Willie Morris", ... | [{"credit_id": "52fe47519251416c750951ab", "de... |  7000000 | [{"id": 35, "name": "Comedy"}, {"id": 18, "nam... |                 http://mydogskip.warnerbros.com/ |  17908 | [{"id": 787, "name": "mississippi"}, {"id": 33... |                en |  ... | [{"name": "Alcon Entertainment", "id": 1088}, ... | [{"iso_3166_1": "US", "name": "United States o... |   2000-01-14 |        0 |    95.0 |       [{"iso_639_1": "en", "name": "English"}] | Released |                   Every family needs an optimist. |          6.5 | 69         |
| 4642 |    44490 |              Chuck & Buck | [{"cast_id": 1, "character": "Buck O'Brien", "... | [{"credit_id": "53463de60e0a265fe6000f2b", "de... |        0 | [{"id": 35, "name": "Comedy"}, {"id": 18, "nam... |                                              NaN |  44490 | [{"id": 237, "name": "gay"}, {"id": 10183, "na... |                en |  ... |                                                [] | [{"iso_3166_1": "US", "name": "United States o... |   2000-01-21 |        0 |    96.0 |       [{"iso_639_1": "en", "name": "English"}] | Released |             REMEMBER THOSE GAMES WE USED TO PLAY? |          5.7 | 16         |
|  ... |      ... |                       ... |                                               ... |                                               ... |      ... |                                               ... |                                              ... |    ... |                                               ... |               ... |  ... |                                               ... |                                               ... |          ... |      ... |     ... |                                            ... |      ... |                                               ... |          ... | ...        |
| 3254 |   385736 |                     Kicks | [{"cast_id": 2, "character": "Marlon", "credit... | [{"credit_id": "570f87d992514102b9002c1e", "de... |        0 |                 [{"id": 12, "name": "Adventure"}] |               http://www.focusfeatures.com/kicks | 385736 | [{"id": 3405, "name": "blow job"}, {"id": 1173... |                en |  ... | [{"name": "Bystorm Films", "id": 2903}, {"name... | [{"iso_3166_1": "US", "name": "United States o... |   2016-09-09 |        0 |    80.0 |       [{"iso_639_1": "en", "name": "English"}] | Released |                            They aren't just shoes |          7.5 | 18         |
| 4726 |   339408 |     The Birth of a Nation | [{"cast_id": 2, "character": "Nat Turner", "cr... | [{"credit_id": "56af01149251417e2900b61c", "de... |  8500000 |                     [{"id": 18, "name": "Drama"}] | http://www.foxsearchlight.com/thebirthofanation/ | 339408 |                 [{"id": 2831, "name": "slavery"}] |                en |  ... | [{"name": "Phantom Four", "id": 423}, {"name":... | [{"iso_3166_1": "US", "name": "United States o... |   2016-09-09 | 15861566 |   120.0 |       [{"iso_639_1": "en", "name": "English"}] | Released |                    The Untold Story of Nat Turner |          6.5 | 178        |
| 3307 |   374461 |                Mr. Church | [{"cast_id": 6, "character": "Henry Church", "... | [{"credit_id": "5710041cc3a3684122000ee4", "de... |  8000000 |                     [{"id": 18, "name": "Drama"}] |                                              NaN | 374461 | [{"id": 1650, "name": "cook"}, {"id": 6054, "n... |                en |  ... | [{"name": "Envision Media Arts", "id": 19456},... | [{"iso_3166_1": "US", "name": "United States o... |   2016-09-16 |        0 |   104.0 |       [{"iso_639_1": "en", "name": "English"}] | Released |  He was the one person she could always count on. |          7.0 | 129        |
| 3413 |   325373 |     Two Lovers and a Bear | [{"cast_id": 0, "character": "Roman", "credit_... | [{"credit_id": "572b7278c3a3684806002e6e", "de... |        0 | [{"id": 18, "name": "Drama"}, {"id": 10749, "n... |                                              NaN | 325373 | [{"id": 1415, "name": "small town"}, {"id": 46... |                en |  ... |                                                [] |                                                [] |   2016-10-02 |        0 |    96.0 |       [{"iso_639_1": "en", "name": "English"}] | Released |                                               NaN |          6.8 | 27         |
| 4262 |   426469 |          Growing Up Smith | [{"cast_id": 4, "character": "Smith Bhatnagar"... | [{"credit_id": "582e0bdfc3a368772600b6c1", "de... |        0 | [{"id": 35, "name": "Comedy"}, {"id": 10751, "... |               http://www.growingupsmithmovie.com | 426469 |                                                [] |                en |  ... |                                                [] |                                                [] |   2017-02-03 |        0 |   102.0 |       [{"iso_639_1": "en", "name": "English"}] | Released |          It’s better to stand out than to fit in. |          7.4 | 7          |

```python
movie_credit['cast'][0] # cast 필드 데이터 확인해보기
```

```
'[{"cast_id": 242, "character": "Jake Sully", "credit_id": "5602a8a7c3a3685532001c9a", "gender": 2, "id": 65731, "name": "Sam Worthington", "order": 0}, {"cast_id": 3, "character": "Neytiri", "credit_id": "52fe48009251416c750ac9cb", "gender": 1, "id": 8691, "name": "Zoe Saldana", "order": 1}, {"cast_id": 25, "character": "Dr. Grace Augustine", "credit_id": "52fe48009251416c750aca39", "gender": 1, "id": 10205, "name": "Sigourney Weaver", "order": 2}, {"cast_id": 4, "character": "Col. Quaritch", "credit_id": "52fe48009251416c750ac9cf", "gender": 2, "id": 32747, "name": "Stephen Lang", "order": 3}, {"cast_id": 5, "character": "Trudy Chacon", "credit_id": "52fe48009251416c750ac9d3", "gender": 1, "id": 17647, "name": "Michelle Rodriguez", "order": 4}, {"cast_id": 8, "character": "Selfridge", "credit_id": "52fe48009251416c750ac9e1", "gender": 2, "id": 1771, "name": "Giovanni Ribisi", "order": 5}, {"cast_id": 7, "character": "Norm Spellman", "credit_id": "52fe48009251416c750ac9dd", "gender": 2, "id": 59231, "name": "Joel David Moore", "order": 6}, {"cast_id": 9, "character": "Moat", "credit_id": "52fe48009251416c750ac9e5", "gender": 1, "id": 30485, "name": "CCH Pounder", "order": 7}, {"cast_id": 11, "character": "Eytukan", "credit_id": "52fe48009251416c750ac9ed", "gender": 2, "id": 15853, "name": "Wes Studi", "order": 8}, {"cast_id": 10, "character": "Tsu\'Tey", "credit_id": "52fe48009251416c750ac9e9", "gender": 2, "id": 10964, "name": "Laz Alonso", "order": 9}, {"cast_id": 12, "character": "Dr. Max Patel", "credit_id": "52fe48009251416c750ac9f1", "gender": 2, "id": 95697, "name": "Dileep Rao", "order": 10}, {"cast_id": 13, "character": "Lyle Wainfleet", "credit_id": "52fe48009251416c750ac9f5", "gender": 2, "id": 98215, "name": "Matt Gerald", "order": 11}, {"cast_id": 32, "character": "Private Fike", "credit_id": "52fe48009251416c750aca5b", "gender": 2, "id": 154153, "name": "Sean Anthony Moran", "order": 12}, {"cast_id": 33, "character": "Cryo Vault Med Tech", "credit_id": "52fe48009251416c750aca5f", "gender": 2, "id": 397312, "name": "Jason Whyte", "order": 13}, {"cast_id": 34, "character": "Venture Star Crew Chief", "credit_id": "52fe48009251416c750aca63", "gender": 2, "id": 42317, "name": "Scott Lawrence", "order": 14}, {"cast_id": 35, "character": "Lock Up Trooper", "credit_id": "52fe48009251416c750aca67", "gender": 2, "id": 986734, "name": "Kelly Kilgour", "order": 15}, {"cast_id": 36, "character": "Shuttle Pilot", "credit_id": "52fe48009251416c750aca6b", "gender": 0, "id": 1207227, "name": "James Patrick Pitt", "order": 16}, {"cast_id": 37, "character": "Shuttle Co-Pilot", "credit_id": "52fe48009251416c750aca6f", "gender": 0, "id": 1180936, "name": "Sean Patrick Murphy", "order": 17}, {"cast_id": 38, "character": "Shuttle Crew Chief", "credit_id": "52fe48009251416c750aca73", "gender": 2, "id": 1019578, "name": "Peter Dillon", "order": 18}, {"cast_id": 39, "character": "Tractor Operator / Troupe", "credit_id": "52fe48009251416c750aca77", "gender": 0, "id": 91443, "name": "Kevin Dorman", "order": 19}, {"cast_id": 40, "character": "Dragon Gunship Pilot", "credit_id": "52fe48009251416c750aca7b", "gender": 2, "id": 173391, "name": "Kelson Henderson", "order": 20}, {"cast_id": 41, "character": "Dragon Gunship Gunner", "credit_id": "52fe48009251416c750aca7f", "gender": 0, "id": 1207236, "name": "David Van Horn", "order": 21}, {"cast_id": 42, "character": "Dragon Gunship Navigator", "credit_id": "52fe48009251416c750aca83", "gender": 0, "id": 215913, "name": "Jacob Tomuri", "order": 22}, {"cast_id": 43, "character": "Suit #1", "credit_id": "52fe48009251416c750aca87", "gender": 0, "id": 143206, "name": "Michael Blain-Rozgay", "order": 23}, {"cast_id": 44, "character": "Suit #2", "credit_id": "52fe48009251416c750aca8b", "gender": 2, "id": 169676, "name": "Jon Curry", "order": 24}, {"cast_id": 46, "character": "Ambient Room Tech", "credit_id": "52fe48009251416c750aca8f", "gender": 0, "id": 1048610, "name": "Luke Hawker", "order": 25}, {"cast_id": 47, "character": "Ambient Room Tech / Troupe", "credit_id": "52fe48009251416c750aca93", "gender": 0, "id": 42288, "name": "Woody Schultz", "order": 26}, {"cast_id": 48, "character": "Horse Clan Leader", "credit_id": "52fe48009251416c750aca97", "gender": 2, "id": 68278, "name": "Peter Mensah", "order": 27}, {"cast_id": 49, "character": "Link Room Tech", "credit_id": "52fe48009251416c750aca9b", "gender": 0, "id": 1207247, "name": "Sonia Yee", "order": 28}, {"cast_id": 50, "character": "Basketball Avatar / Troupe", "credit_id": "52fe48009251416c750aca9f", "gender": 1, "id": 1207248, "name": "Jahnel Curfman", "order": 29}, {"cast_id": 51, "character": "Basketball Avatar", "credit_id": "52fe48009251416c750acaa3", "gender": 0, "id": 89714, "name": "Ilram Choi", "order": 30}, {"cast_id": 52, "character": "Na\'vi Child", "credit_id": "52fe48009251416c750acaa7", "gender": 0, "id": 1207249, "name": "Kyla Warren", "order": 31}, {"cast_id": 53, "character": "Troupe", "credit_id": "52fe48009251416c750acaab", "gender": 0, "id": 1207250, "name": "Lisa Roumain", "order": 32}, {"cast_id": 54, "character": "Troupe", "credit_id": "52fe48009251416c750acaaf", "gender": 1, "id": 83105, "name": "Debra Wilson", "order": 33}, {"cast_id": 57, "character": "Troupe", "credit_id": "52fe48009251416c750acabb", "gender": 0, "id": 1207253, "name": "Chris Mala", "order": 34}, {"cast_id": 55, "character": "Troupe", "credit_id": "52fe48009251416c750acab3", "gender": 0, "id": 1207251, "name": "Taylor Kibby", "order": 35}, {"cast_id": 56, "character": "Troupe", "credit_id": "52fe48009251416c750acab7", "gender": 0, "id": 1207252, "name": "Jodie Landau", "order": 36}, {"cast_id": 58, "character": "Troupe", "credit_id": "52fe48009251416c750acabf", "gender": 0, "id": 1207254, "name": "Julie Lamm", "order": 37}, {"cast_id": 59, "character": "Troupe", "credit_id": "52fe48009251416c750acac3", "gender": 0, "id": 1207257, "name": "Cullen B. Madden", "order": 38}, {"cast_id": 60, "character": "Troupe", "credit_id": "52fe48009251416c750acac7", "gender": 0, "id": 1207259, "name": "Joseph Brady Madden", "order": 39}, {"cast_id": 61, "character": "Troupe", "credit_id": "52fe48009251416c750acacb", "gender": 0, "id": 1207262, "name": "Frankie Torres", "order": 40}, {"cast_id": 62, "character": "Troupe", "credit_id": "52fe48009251416c750acacf", "gender": 1, "id": 1158600, "name": "Austin Wilson", "order": 41}, {"cast_id": 63, "character": "Troupe", "credit_id": "52fe48019251416c750acad3", "gender": 1, "id": 983705, "name": "Sara Wilson", "order": 42}, {"cast_id": 64, "character": "Troupe", "credit_id": "52fe48019251416c750acad7", "gender": 0, "id": 1207263, "name": "Tamica Washington-Miller", "order": 43}, {"cast_id": 65, "character": "Op Center Staff", "credit_id": "52fe48019251416c750acadb", "gender": 1, "id": 1145098, "name": "Lucy Briant", "order": 44}, {"cast_id": 66, "character": "Op Center Staff", "credit_id": "52fe48019251416c750acadf", "gender": 2, "id": 33305, "name": "Nathan Meister", "order": 45}, {"cast_id": 67, "character": "Op Center Staff", "credit_id": "52fe48019251416c750acae3", "gender": 0, "id": 1207264, "name": "Gerry Blair", "order": 46}, {"cast_id": 68, "character": "Op Center Staff", "credit_id": "52fe48019251416c750acae7", "gender": 2, "id": 33311, "name": "Matthew Chamberlain", "order": 47}, {"cast_id": 69, "character": "Op Center Staff", "credit_id": "52fe48019251416c750acaeb", "gender": 0, "id": 1207265, "name": "Paul Yates", "order": 48}, {"cast_id": 70, "character": "Op Center Duty Officer", "credit_id": "52fe48019251416c750acaef", "gender": 0, "id": 1207266, "name": "Wray Wilson", "order": 49}, {"cast_id": 71, "character": "Op Center Staff", "credit_id": "52fe48019251416c750acaf3", "gender": 2, "id": 54492, "name": "James Gaylyn", "order": 50}, {"cast_id": 72, "character": "Dancer", "credit_id": "52fe48019251416c750acaf7", "gender": 0, "id": 1207267, "name": "Melvin Leno Clark III", "order": 51}, {"cast_id": 73, "character": "Dancer", "credit_id": "52fe48019251416c750acafb", "gender": 0, "id": 1207268, "name": "Carvon Futrell", "order": 52}, {"cast_id": 74, "character": "Dancer", "credit_id": "52fe48019251416c750acaff", "gender": 0, "id": 1207269, "name": "Brandon Jelkes", "order": 53}, {"cast_id": 75, "character": "Dancer", "credit_id": "52fe48019251416c750acb03", "gender": 0, "id": 1207270, "name": "Micah Moch", "order": 54}, {"cast_id": 76, "character": "Dancer", "credit_id": "52fe48019251416c750acb07", "gender": 0, "id": 1207271, "name": "Hanniyah Muhammad", "order": 55}, {"cast_id": 77, "character": "Dancer", "credit_id": "52fe48019251416c750acb0b", "gender": 0, "id": 1207272, "name": "Christopher Nolen", "order": 56}, {"cast_id": 78, "character": "Dancer", "credit_id": "52fe48019251416c750acb0f", "gender": 0, "id": 1207273, "name": "Christa Oliver", "order": 57}, {"cast_id": 79, "character": "Dancer", "credit_id": "52fe48019251416c750acb13", "gender": 0, "id": 1207274, "name": "April Marie Thomas", "order": 58}, {"cast_id": 80, "character": "Dancer", "credit_id": "52fe48019251416c750acb17", "gender": 0, "id": 1207275, "name": "Bravita A. Threatt", "order": 59}, {"cast_id": 81, "character": "Mining Chief (uncredited)", "credit_id": "52fe48019251416c750acb1b", "gender": 0, "id": 1207276, "name": "Colin Bleasdale", "order": 60}, {"cast_id": 82, "character": "Veteran Miner (uncredited)", "credit_id": "52fe48019251416c750acb1f", "gender": 0, "id": 107969, "name": "Mike Bodnar", "order": 61}, {"cast_id": 83, "character": "Richard (uncredited)", "credit_id": "52fe48019251416c750acb23", "gender": 0, "id": 1207278, "name": "Matt Clayton", "order": 62}, {"cast_id": 84, "character": "Nav\'i (uncredited)", "credit_id": "52fe48019251416c750acb27", "gender": 1, "id": 147898, "name": "Nicole Dionne", "order": 63}, {"cast_id": 85, "character": "Trooper (uncredited)", "credit_id": "52fe48019251416c750acb2b", "gender": 0, "id": 1207280, "name": "Jamie Harrison", "order": 64}, {"cast_id": 86, "character": "Trooper (uncredited)", "credit_id": "52fe48019251416c750acb2f", "gender": 0, "id": 1207281, "name": "Allan Henry", "order": 65}, {"cast_id": 87, "character": "Ground Technician (uncredited)", "credit_id": "52fe48019251416c750acb33", "gender": 2, "id": 1207282, "name": "Anthony Ingruber", "order": 66}, {"cast_id": 88, "character": "Flight Crew Mechanic (uncredited)", "credit_id": "52fe48019251416c750acb37", "gender": 0, "id": 1207283, "name": "Ashley Jeffery", "order": 67}, {"cast_id": 14, "character": "Samson Pilot", "credit_id": "52fe48009251416c750ac9f9", "gender": 0, "id": 98216, "name": "Dean Knowsley", "order": 68}, {"cast_id": 89, "character": "Trooper (uncredited)", "credit_id": "52fe48019251416c750acb3b", "gender": 0, "id": 1201399, "name": "Joseph Mika-Hunt", "order": 69}, {"cast_id": 90, "character": "Banshee (uncredited)", "credit_id": "52fe48019251416c750acb3f", "gender": 0, "id": 236696, "name": "Terry Notary", "order": 70}, {"cast_id": 91, "character": "Soldier (uncredited)", "credit_id": "52fe48019251416c750acb43", "gender": 0, "id": 1207287, "name": "Kai Pantano", "order": 71}, {"cast_id": 92, "character": "Blast Technician (uncredited)", "credit_id": "52fe48019251416c750acb47", "gender": 0, "id": 1207288, "name": "Logan Pithyou", "order": 72}, {"cast_id": 93, "character": "Vindum Raah (uncredited)", "credit_id": "52fe48019251416c750acb4b", "gender": 0, "id": 1207289, "name": "Stuart Pollock", "order": 73}, {"cast_id": 94, "character": "Hero (uncredited)", "credit_id": "52fe48019251416c750acb4f", "gender": 0, "id": 584868, "name": "Raja", "order": 74}, {"cast_id": 95, "character": "Ops Centreworker (uncredited)", "credit_id": "52fe48019251416c750acb53", "gender": 0, "id": 1207290, "name": "Gareth Ruck", "order": 75}, {"cast_id": 96, "character": "Engineer (uncredited)", "credit_id": "52fe48019251416c750acb57", "gender": 0, "id": 1062463, "name": "Rhian Sheehan", "order": 76}, {"cast_id": 97, "character": "Col. Quaritch\'s Mech Suit (uncredited)", "credit_id": "52fe48019251416c750acb5b", "gender": 0, "id": 60656, "name": "T. J. Storm", "order": 77}, {"cast_id": 98, "character": "Female Marine (uncredited)", "credit_id": "52fe48019251416c750acb5f", "gender": 0, "id": 1207291, "name": "Jodie Taylor", "order": 78}, {"cast_id": 99, "character": "Ikran Clan Leader (uncredited)", "credit_id": "52fe48019251416c750acb63", "gender": 1, "id": 1186027, "name": "Alicia Vela-Bailey", "order": 79}, {"cast_id": 100, "character": "Geologist (uncredited)", "credit_id": "52fe48019251416c750acb67", "gender": 0, "id": 1207292, "name": "Richard Whiteside", "order": 80}, {"cast_id": 101, "character": "Na\'vi (uncredited)", "credit_id": "52fe48019251416c750acb6b", "gender": 0, "id": 103259, "name": "Nikie Zambo", "order": 81}, {"cast_id": 102, "character": "Ambient Room Tech / Troupe", "credit_id": "52fe48019251416c750acb6f", "gender": 1, "id": 42286, "name": "Julene Renee", "order": 82}]'
```

```python
# cast 데이터를 name만 뽑아서 따로 정리하기
import json


for i in range(len(movie_credit)):
    json_data = json.loads(movie_credit['cast'][i])
    tmp = []
    for name in json_data[:min(10, len(json_data))]:
        tmp += [name["name"]]
    movie_credit["cast"][i] = tmp
```

```
9 Final Fantasy: The Spirits Within ['Donald Sutherland', 'Ming-Na Wen', 'Alec Baldwin', 'Ving Rhames', 'Steve Buscemi', 'Peri Gilpin', 'James Woods', 'Jean Simmons', 'Keith David']
8 The Croods ['Nicolas Cage', 'Emma Stone', 'Ryan Reynolds', 'Catherine Keener', 'Cloris Leachman', 'Clark Duke', 'Chris Sanders', 'Randy Thom']
7 Gravity ['Sandra Bullock', 'George Clooney', 'Ed Harris', 'Orto Ignatiussen', 'Phaldut Sharma', 'Amy Warren', 'Basher Savage']
7 Son of the Mask ['Jamie Kennedy', 'Alan Cumming', 'Traylor Howard', 'Kal Penn', 'Steven Wright', 'Bob Hoskins', 'Ben Stein']
6 The Spanish Prisoner ['Steve Martin', 'Campbell Scott', 'Ben Gazzara', 'Rebecca Pidgeon', 'Ricky Jay', 'Felicity Huffman']
8 The Flowers of War ['Christian Bale', 'Ni Ni', 'Tong Dawei', 'Zhang Xinyi', 'Shigeo Kobayashi', 'Atsuro Watabe', 'Shawn Dou', 'Paul Schneider']
9 The Spiderwick Chronicles ['Freddie Highmore', 'Mary-Louise Parker', 'Nick Nolte', 'Sarah Bolger', 'Andrew McCarthy', 'Joan Plowright', 'David Strathairn', 'Seth Rogen', 'Martin Short']
5 102 Dalmatians ['Glenn Close', 'Ioan Gruffudd', 'Alice Evans', 'Tim McInnerny', 'Gérard Depardieu']
7 Evolution ['Max Brebant', 'Roxane Duran', 'Julie-Marie Parmentier', 'Mathieu Goldfeld', 'Nissim Renard', 'Pablo-Noé Etienne', 'Nathalie Legosles']
6 The Edge ['Alec Baldwin', 'Anthony Hopkins', 'Elle Macpherson', 'Harold Perrineau', 'L.Q. Jones', 'Kathleen Wilhoite']
6 Thirteen Days ['Kevin Costner', 'Bruce Greenwood', 'Steven Culp', 'Dylan Baker', 'Shawn Driscoll', 'Drake Cook']
9 Red Planet ['Val Kilmer', 'Carrie-Anne Moss', 'Benjamin Bratt', 'Tom Sizemore', 'Simon Baker', 'Terence Stamp', 'Jessica Morton', 'Caroline Bossi', 'Bob Neill']
8 Oceans ['Pierce Brosnan', 'Jacques Perrin', 'Rie Miyazawa', 'Aldo Baglio', 'Matthias Brandt', 'Lancelot Perrin', 'Manolo Garcia', 'Pedro Armendáriz Jr.']
6 Top Cat Begins ['Jason Harris', 'David Hoffman', 'Bill Lobley', 'Darin De Paul', 'Marieve Herington', 'David Boat']
8 Titan A.E. ['Matt Damon', 'Bill Pullman', 'Drew Barrymore', 'John Leguizamo', 'Nathan Lane', 'Janeane Garofalo', 'Ron Perlman', 'Alex D. Linz']
9 I Spy ['Eddie Murphy', 'Owen Wilson', 'Famke Janssen', 'Keith Dallas', 'Malcolm McDowell', 'Crystal Lowe', 'Gary Cole', 'Bill Mondy', 'Lynda Boyd']
5 Ballistic: Ecks vs. Sever ['Antonio Banderas', 'Lucy Liu', 'Gregg Henry', 'Ray Park', 'Talisa Soto']
8 Osmosis Jones ['Chris Rock', 'Laurence Fishburne', 'David Hyde Pierce', 'Brandy Norwood', 'Bill Murray', 'Molly Shannon', 'William Shatner', 'Ron Howard']
9 Proof of Life ['Meg Ryan', 'Russell Crowe', 'David Morse', 'Pamela Reed', 'David Caruso', 'Flora Martínez', 'Anthony Heald', 'Gottfried John', 'Tony Vázquez']
8 We Are Marshall ['Matthew McConaughey', 'Matthew Fox', 'Anthony Mackie', 'David Strathairn', 'Ian McShane', 'Kate Mara', 'January Jones', 'Kate Kneeland']
8 Hudson Hawk ['Bruce Willis', 'Danny Aiello', 'Andie MacDowell', 'James Coburn', 'Richard E. Grant', 'Sandra Bernhard', 'David Caruso', 'Frank Stallone']
6 Little Man ['Marlon Wayans', 'Shawn Wayans', 'Kerry Washington', 'John Witherspoon', 'Tracy Morgan', 'Lochlyn Munro']
8 Cats & Dogs ['Jeff Goldblum', 'Elizabeth Perkins', 'Alexander Pollock', 'Miriam Margolyes', 'Tobey Maguire', 'Alec Baldwin', 'Susan Sarandon', 'Charlton Heston']
7 Kangaroo Jack ["Jerry O'Connell", 'Anthony Anderson', 'Estella Warren', 'Christopher Walken', 'Michael Shannon', 'Marton Csokas', 'Dyan Cannon']
8 Coraline ['Dakota Fanning', 'Teri Hatcher', 'Jennifer Saunders', 'Dawn French', 'Keith David', 'John Hodgman', 'Robert Bailey Jr.', 'Ian McShane']
8 My Favorite Martian ['Jeff Daniels', 'Elizabeth Hurley', 'Daryl Hannah', 'Christopher Lloyd', 'Wallace Shawn', 'Christine Ebersole', 'Michael Lerner', 'T. K. Carter']
5 Holy Man ['Eddie Murphy', 'Jeff Goldblum', 'Kelly Preston', 'Robert Loggia', 'Jon Cryer']
5 The Hunted ['Tommy Lee Jones', 'Benicio del Toro', 'Connie Nielsen', 'Leslie Stefanson', 'John Finn']
9 The Phantom of the Opera ['Gerard Butler', 'Emmy Rossum', 'Patrick Wilson', 'Miranda Richardson', 'Minnie Driver', 'Ciarán Hinds', 'Simon Callow', 'Victor McGuire', 'Jennifer Ellison']
9 Domestic Disturbance ['John Travolta', 'Vince Vaughn', 'Teri Polo', "Matt O'Leary", 'Steve Buscemi', 'James Lashly', 'Rebecca Tilney', 'Debra Mooney', 'Rodney Pike']
9 Beloved ['Oprah Winfrey', 'Danny Glover', 'Thandie Newton', 'Lisa Gay Hamilton', 'Albert Hall', 'Irma P. Hall', 'Kimberly Elise', 'Beah Richards', 'Vertamae Grosvenor']
8 Lucky You ['Eric Bana', 'Drew Barrymore', 'Robert Duvall', 'Debra Messing', 'Robert Downey Jr.', 'Phyllis Somerville', 'Horatio Sanz', 'Michael Shannon']
8 The Adventures of Sharkboy and Lavagirl ['Taylor Lautner', 'Taylor Dooley', 'Cayden Boyd', 'David Arquette', 'Kristin Davis', 'Jacob Davich', 'Sasha Pieterse', 'George Lopez']
7 For Love of the Game ['Kevin Costner', 'Kelly Preston', 'John C. Reilly', 'Jena Malone', 'J.K. Simmons', 'Brian Cox', 'David Mucci']
7 The Host ['Song Kang-ho', 'Park Hae-il', 'Bae Doona', 'Ko Ah-sung', 'Byun Hee-bong', 'Scott Wilson', 'Paul Lazar']
7 The Host ['Song Kang-ho', 'Park Hae-il', 'Bae Doona', 'Ko Ah-sung', 'Byun Hee-bong', 'Scott Wilson', 'Paul Lazar']
9 Into the Blue ['Paul Walker', 'Jessica Alba', 'Scott Caan', 'Ashley Scott', 'Josh Brolin', 'Chris Taloa', 'James Frain', 'Dwayne Adway', 'Tyson Beckford']
8 Baby's Day Out ['Joe Mantegna', 'Lara Flynn Boyle', 'Joe Pantoliano', 'Brian Haley', 'Cynthia Nixon', 'John Neville', 'William Holmes', 'Anna Levine']
7 Street Fighter: The Legend of Chun-Li ['Kristin Kreuk', 'Chris Klein', 'Neal McDonough', 'Michael Clarke Duncan', 'Moon Bloodgood', 'Robin Shou', 'Josie Ho']
9 Yours, Mine and Ours ['Lucille Ball', 'Henry Fonda', 'Van Johnson', 'Tom Bosley', 'Louise Troy', 'Sidney Miller', 'Morgan Brittany', 'Tracy Nelson', 'Tim Matheson']
7 Last Holiday ['Queen Latifah', 'LL Cool J', 'Timothy Hutton', 'Giancarlo Esposito', 'Alicia Witt', 'Gérard Depardieu', 'Jane Adams']
8 All the Pretty Horses ['Matt Damon', 'Henry Thomas', 'Penélope Cruz', 'Sam Shepard', 'Robert Patrick', 'Lucas Black', 'Jesse Plemons', 'Rubén Blades']
8 Curse of the Golden Flower ['Chow Yun-fat', 'Gong Li', 'Jay Chou', 'Liu Ye', 'Qin Jun-Jie', 'Li Man', 'Ni Dahong', 'Chen Jin']
8 The Mirror Has Two Faces ['Barbra Streisand', 'Jeff Bridges', 'Lauren Bacall', 'George Segal', 'Mimi Rogers', 'Pierce Brosnan', 'Brenda Vaccaro', 'Elle Mcpherson']
8 Double Jeopardy ['Tommy Lee Jones', 'Ashley Judd', 'Bruce Greenwood', 'Annabeth Gish', 'Benjamin Weir', 'Jay Brazeau', 'John Maclaren', 'Tracy Vilar']
7 Eight Below ['Paul Walker', 'Bruce Greenwood', 'Moon Bloodgood', 'Jason Biggs', 'Gerard Plunkett', 'August Schellenberg', 'Wendy Crewson']
8 Big Momma's House 2 ['Martin Lawrence', 'Nia Long', 'Emily Procter', 'Zachary Levi', 'Mark Moses', 'Kat Dennings', 'Chloë Grace Moretz', 'Marisol Nichols']
7 The Art of War ['Wesley Snipes', 'Donald Sutherland', 'Maury Chaykin', 'Anne Archer', 'Michael Biehn', 'Cary-Hiroyuki Tagawa', 'Marie Matiko']
8 City By The Sea ['Robert De Niro', 'James Franco', 'Frances McDormand', 'Eliza Dushku', 'George Dzundza', 'Patti LuPone', 'Linda Emond', 'Stephi Lineburg']
7 City Hall ['Al Pacino', 'John Cusack', 'Bridget Fonda', 'Danny Aiello', 'Martin Landau', 'David Paymer', 'Richard Schiff']
9 Raise the Titanic ['M. Emmet Walsh', 'Richard Jordan', 'David Selby', 'Anne Archer', 'Alec Guinness', 'Bo Brundin', 'Jason Robards', 'Michael Ensign', 'Maurice Kowalewski']
9 Nomad: The Warrior ['Kuno Becker', 'Jay Hernandez', 'Jason Scott Lee', 'Doskhan Zholzhaksynov', 'Ayanat Ksenbai', 'Mark Dacascos', 'Aziz Beyshenaliev', 'Erik Zholzhaksynov', 'Dilnaz Akhmadieva']
9 A Monster in Paris ['Vanessa Paradis', 'Mathieu Chedid', 'Gad Elmaleh', 'François Cluzet', 'Ludivine Sagnier', 'Julie Ferrier', 'Bruno Salomone', 'Sébastien Desjours', 'Philippe Peythieu']
7 Against the Ropes ['Meg Ryan', 'Tony Shalhoub', 'Joe Cortese', 'Kerry Washington', 'Omar Epps', 'Charles S. Dutton', 'Tim Daly']
9 Dragon Nest: Warriors' Dawn ['Carrie-Anne Moss', 'Lucas Grabeel', 'Blythe Auffarth', 'Charlie Schlatter', 'Simon Jaglom', 'Matthew Temple', 'Ying Huang', 'Ye Sun', 'Bianca Collins']
8 The Express ['Rob Brown', 'Dennis Quaid', 'Darrin Henson', 'Charles S. Dutton', 'Aunjanue Ellis', 'Omar Benson Miller', 'Clancy Brown', 'Chadwick Boseman']
8 Isn't She Great ['Bette Midler', 'Nathan Lane', 'Stockard Channing', 'David Hyde Pierce', 'John Cleese', 'John Larroquette', 'Amanda Peet', 'Dina Spybey-Waters']
7 Guess Who ['Bernie Mac', 'Ashton Kutcher', 'Zoe Saldana', 'Judith Scott', 'Hal Williams', 'Kellee Stewart', 'Jessica Cauffiel']
6 Radio ['Cuba Gooding Jr.', 'Ed Harris', 'Alfre Woodard', 'S. Epatha Merkerson', 'Debra Winger', 'Chris Mulkey']
9 Mirrors ['Kiefer Sutherland', 'Paula Patton', 'Amy Smart', 'Cameron Boyce', 'Erica Gluck', 'Jason Flemyng', 'Darren Kent', 'Ezra Buzzington', 'Julian Glover']
8 Lions for Lambs ['Robert Redford', 'Meryl Streep', 'Tom Cruise', 'Michael Peña', 'Andrew Garfield', 'Peter Berg', 'Derek Luke', 'Jennifer Sommerfeld']
5 Flight of the Intruder ['Danny Glover', 'Willem Dafoe', 'Brad Johnson', 'Rosanna Arquette', 'Tom Sizemore']
6 Knock Off ['Jean-Claude Van Damme', 'Lela Rochon', 'Paul Sorvino', 'Rob Schneider', 'Mark Houghton', 'Kim-Maree Penn']
4 Warriors of Virtue ['Angus Macfadyen', 'Mario Yedidia', 'Marley Shelton', 'Chao Li Chi']
9 Black Water Transit ['Laurence Fishburne', 'Karl Urban', 'Brittany Snow', 'Aisha Tyler', "Beverly D'Angelo", 'Evan Ross', 'Stephen Dorff', 'Leslie Easterbrook', 'Bill Cobbs']
9 Chill Factor ['Cuba Gooding Jr.', 'Skeet Ulrich', 'Peter Firth', 'David Paymer', 'Daniel Hugh Kelly', 'Judson Mills', 'Jordan Mott', 'Hudson Leick', "Kevin J. O'Connor"]
8 I Dreamed of Africa ['Kim Basinger', 'Vincent Pérez', 'Liam Aiken', 'Daniel Craig', 'Eva Marie Saint', 'Lance Reddick', 'Stephen Jennings', 'Nick Boraine']
6 Big Momma's House ['Martin Lawrence', 'Nia Long', 'Paul Giamatti', 'Jascha Washington', 'Terrence Howard', 'Octavia Spencer']
5 Pushing Tin ['John Cusack', 'Billy Bob Thornton', 'Cate Blanchett', 'Angelina Jolie', 'Gene Dinovi']
9 Snow Dogs ['Jim Belushi', 'Cuba Gooding Jr.', 'James Coburn', 'M. Emmet Walsh', 'Sisqó', 'Nichelle Nichols', 'Graham Greene', 'Brian Doyle-Murray', 'Angela Moore']
7 Dreamer: Inspired By a True Story ['Kurt Russell', 'Dakota Fanning', 'Kris Kristofferson', 'Elisabeth Shue', 'David Morse', 'Freddy Rodríguez', 'Luis Guzmán']
7 Laws of Attraction ['Pierce Brosnan', 'Julianne Moore', 'Michael Sheen', 'Parker Posey', 'Frances Fisher', 'Nora Dunn', 'Annika Pergament']
9 Bogus ['Whoopi Goldberg', 'Gérard Depardieu', 'Haley Joel Osment', 'Ute Lemper', 'Andrea Martin', 'Nancy Travis', 'Denis Mercier', 'Sheryl Lee Ralph', 'Barbara Hamilton']
5 Cats Don't Dance ['Scott Bakula', 'Jasmine Guy', 'Natalie Cole', 'Ashley Peldon', 'Lindsay Ridgeway']
9 The Prince of Tides ['Nick Nolte', 'Barbra Streisand', 'Blythe Danner', 'Kate Nelligan', 'Jeroen Krabbé', 'Melinda Dillon', 'George Carlin', 'Jason Gould', 'Nancy Moore Atchison']
8 Midnight Run ['Robert De Niro', 'Charles Grodin', 'Yaphet Kotto', 'John Ashton', 'Dennis Farina', 'Joe Pantoliano', 'Richard Foronjy', 'Philip Baker Hall']
8 Take the Lead ['Antonio Banderas', 'Rob Brown', 'Yaya DaCosta', 'Alfre Woodard', 'John Ortiz', 'Laura Benanti', 'Katya Virshilas', 'Jenna Dewan']
7 One True Thing ['Meryl Streep', 'Renée Zellweger', 'William Hurt', 'Tom Everett Scott', 'Lauren Graham', 'Julianne Nicholson', 'Jeffrey Scaperrotta']
8 Splice ['Adrien Brody', 'Sarah Polley', 'Delphine Chanéac', 'David Hewlett', 'Abigail Chu', 'Stephanie Baird', 'Brandon McGibbon', 'Amanda Brugel']
8 Godsend ['Greg Kinnear', 'Rebecca Romijn', 'Robert De Niro', 'Cameron Bright', 'Zoie Palmer', 'Munro Chambers', 'Andrew Chalmers', 'Marcia Bennett']
6 The Promise ['Cecilia Cheung', 'Liu Ye', 'Hong Chen', 'Cheng Qian', 'Jang Dong-gun', 'Hiroyuki Sanada']
7 Animals United ['Christoph Maria Herbst', 'Ralf Schmitz', 'Thomas Fritsch', 'Bastian Pastewka', 'Oliver Kalkofe', 'Nana Spier', 'Constantin von Jascheroff']
5 Goodbye Bafana ['Joseph Fiennes', 'Dennis Haysbert', 'Diane Kruger', 'Shiloh Henderson', 'Patrick Lyster']
9 United Passions ['Tim Roth', 'Sam Neill', 'Thomas Kretschmann', 'Gérard Depardieu', 'Jemima West', 'Karina Lombard', 'Fisher Stevens', 'Benedict Freitag', 'Jonathan Louis']
7 Ripley's Game ['John Malkovich', 'Ray Winstone', 'Uwe Mansshardt', 'Hanns Zischler', 'Paolo Paoloni', 'Lena Headey', 'Dougray Scott']
7 Serving Sara ['Matthew Perry', 'Elizabeth Hurley', 'Vincent Pastore', 'Bruce Campbell', 'Cedric the Entertainer', 'Amy Adams', 'Jerry Stiller']
2 Winged Migration ['Philippe Labro', 'Jacques Perrin']
9 A Simple Wish ['Martin Short', 'Kathleen Turner', 'Mara Wilson', 'Robert Pastorelli', 'Deborah Odell', 'Francis Capra', 'Ruby Dee', 'Amanda Plummer', 'Teri Garr']
5 Kundun ['Tenzin Thuthob Tsarong', 'Tencho Gyalpo', 'Tsewang Migyur Khangsar', 'Gyurme Tethong', 'Robert Lin']
7 A Passage to India ['Judy Davis', 'Alec Guinness', 'Peggy Ashcroft', 'James Fox', 'Victor Banerjee', 'Nigel Havers', 'Michael Culver']
6 Suspect Zero ['Carrie-Anne Moss', 'Aaron Eckhart', 'Ben Kingsley', 'Harry Lennix', 'Kevin Chamberlin', 'Keith Campbell']
5 Flawless ['Robert De Niro', 'Philip Seymour Hoffman', 'Barry Miller', 'Chris Bauer', 'Skipp Sudduth']
8 Highlander: The Final Dimension ['Christopher Lambert', 'Mario Van Peebles', 'Deborah Kara Unger', 'Mako', 'Martin Neufeld', 'Daniel Do', 'Michael Jayston', 'Louis Bertignac']
8 Blood and Wine ['Jack Nicholson', 'Stephen Dorff', 'Jennifer Lopez', 'Judy Davis', 'Michael Caine', 'Harold Perrineau', 'Robyn Peterson', 'Mike Starr']
9 Snow White: A Tale of Terror ['Sigourney Weaver', 'Sam Neill', 'Monica Keena', 'Gil Bellows', 'Brian Glover', 'David Conrad', 'Anthony Brophy', 'Andrew Tiernan', 'Taryn Davis']
7 Flipper ['Elijah Wood', 'Paul Hogan', 'Jonathan Banks', 'Jason Fuchs', 'Robert Deacon', 'Luke Halpin', 'Chelsea Field']
9 Nothing to Lose ['Tim Robbins', 'Martin Lawrence', 'John C. McGinley', 'Kelly Preston', 'Irma P. Hall', 'Giancarlo Esposito', 'Michael McKean', 'Rebecca Gayheart', 'Steve Oedekerk']
5 Money Talks ['Chris Tucker', 'Charlie Sheen', 'Heather Locklear', 'Paul Sorvino', 'Elise Neal']
9 Cradle 2 the Grave ['Jet Li', 'DMX', 'Kelly Hu', 'Anthony Anderson', 'Tom Arnold', 'Mark Dacascos', 'Gabrielle Union', 'Johnny Trí Nguyễn', 'Sean Cory Cooper']
8 Mr. Bean's Holiday ['Rowan Atkinson', 'Max Baldry', 'Emma de Caunes', 'Willem Dafoe', 'Karel Roden', 'Steve Pemberton', 'Jean Rochefort', 'Michel Winogradoff']
9 Dear John ['Amanda Seyfried', 'Channing Tatum', 'Henry Thomas', 'Richard Jenkins', 'Scott Porter', 'Keith Robinson', 'Luke Benward', 'David Andrews', 'D.J. Cotrona']
9 Don't Be Afraid of the Dark ['Katie Holmes', 'Guy Pearce', 'Bailee Madison', 'Alan Dale', 'Jack Thompson', 'Emelia Burns', 'Eddie Ritchard', 'Nicholas Bell', 'James Mackay']
9 The Adventures of Pinocchio ['Martin Landau', 'Jonathan Taylor Thomas', 'Geneviève Bujold', 'Udo Kier', 'Bebe Neuwirth', 'Rob Schneider', 'Corey Carrier', 'David Doyle', 'Dawn French']
6 The Greatest Game Ever Played ['Shia LaBeouf', 'Stephen Dillane', 'Josh Flitter', 'Peter Firth', 'Peyton List', 'Elias Koteas']
5 The Ruins ['Shawn Ashmore', 'Jonathan Tucker', 'Jena Malone', 'Laura Ramsey', 'Joe Anderson']
8 Sheena ['Tanya Roberts', 'Ted Wass', 'Donovan Scott', 'Elizabeth of Toro', 'France Zobda', 'Trevor Thomas', 'Clifton Jones', 'John Forgeham']
7 Underclassman ['Nick Cannon', 'Roselyn Sánchez', 'Shawn Ashmore', 'Cheech Marin', 'Kelly Hu', 'Kaylee DeFer', 'Ian Gomez']
7 King's Ransom ['Anthony Anderson', 'Jay Mohr', 'Kellita Smith', "Brooke D'Orsay", 'Donald Faison', 'Christian Potenza', 'Glenn Bang']
6 Carnage ['Kate Winslet', 'Jodie Foster', 'Christoph Waltz', 'John C. Reilly', 'Elvis Polanski', 'Eliot Berger']
7 Cirque du Soleil: Worlds Away ['Erica Linz', 'Igor Zaripov', 'Matt Gillanders', 'Jason Berrent', 'Dallas Barnett', 'Sophia Elisabeth', 'Lutz Halbhubner']
5 The True Story of Puss 'n Boots ['Jérôme Deschamps', 'Yolande Moreau', 'Louise Wallon', 'Arthur Deschamps', 'Jean-Claude Bolle-Reddat']
7 Double Take ['Orlando Jones', 'Eddie Griffin', 'Garcelle Beauvais', 'Gary Grubbs', 'Daniel Roebuck', 'Edward Herrmann', 'Carlos Carrasco']
8 Beyond the Sea ['Kevin Spacey', 'Kate Bosworth', 'John Goodman', 'Bob Hoskins', 'Brenda Blethyn', 'Greta Scacchi', 'Michael Byrne', 'Caroline Aaron']
9 Meet the Deedles ['Paul Walker', 'John Ashton', 'Dennis Hopper', 'Eric Braeden', 'Richard Lineback', 'Robert Englund', 'M.C. Gainey', 'Steve Van Wormer', 'A. J. Langer']
9 The Rookie ['Dennis Quaid', 'Rachel Griffiths', 'Beth Grant', 'Angus T. Jones', 'Brian Cox', 'Chad Lindberg', 'Angelo Spizzirri', 'Jay Hernandez', 'Rick Gonzalez']
9 The Little Vampire ['Richard E. Grant', 'Jonathan Lipnicki', 'Jim Carter', 'Alice Krige', 'Pamela Gidley', 'Tommy Hinkley', 'Anna Popplewell', 'Dean Cook', 'Iain De Caestecker']
7 Darling Lili ['Julie Andrews', 'Rock Hudson', 'Jeremy Kemp', 'Lance Percival', 'Michael Witney', 'Gloria Paul', 'Jacques Marin']
9 Mad Money ['Diane Keaton', 'Queen Latifah', 'Katie Holmes', 'Ted Danson', 'Roger Cross', 'Stephen Root', 'J.C. MacKenzie', 'Christopher McDonald', 'Finesse Mitchell']
7 The Beaver ['Jodie Foster', 'Mel Gibson', 'Jennifer Lawrence', 'Anton Yelchin', 'Zachary Booth', 'Riley Thomas Stewart', 'Kelly Coffield Park']
9 The Jungle Book 2 ['John Goodman', 'Haley Joel Osment', 'Mae Whitman', 'Connor Funk', 'Bob Joles', 'Tony Jay', 'Phil Collins', 'John Rhys-Davies', 'Jim Cummings']
8 The Tigger Movie ['Jim Cummings', 'Nikita Hopkins', 'Ken Sansom', 'John Fiedler', 'Peter Cullen', 'Andre Stojka', 'Kath Soucie', 'Tom Attenborough']
9 The Black Hole ['Maximilian Schell', 'Anthony Perkins', 'Robert Forster', 'Joseph Bottoms', 'Ernest Borgnine', 'Yvette Mimieux', 'Tom McLoughlin', 'Roddy McDowall', 'Slim Pickens']
6 Team America: World Police ['Trey Parker', 'Matt Stone', 'Kristen Miller', 'Masasa Moyo', 'Daran Norris', 'Maurice LaMarche']
9 The Debt ['Helen Mirren', 'Ciarán Hinds', 'Tom Wilkinson', 'Jessica Chastain', 'Sam Worthington', 'Marton Csokas', 'Jesper Christensen', 'Romi Aboulafia', 'Adar Beck']
8 Quigley Down Under ['Tom Selleck', 'Laura San Giacomo', 'Alan Rickman', 'Chris Haywood', 'Ron Haddrick', 'Tony Bonner', 'Ben Mendelsohn', 'Michael Carman']
5 Simon Birch ['Jim Carrey', 'Ashley Judd', 'Ian Michael Smith', 'Joseph Mazzello', 'Oliver Platt']
8 Pooh's Heffalump Movie ['Jim Cummings', 'John Fiedler', 'Nikita Hopkins', 'Kath Soucie', 'Ken Sansom', 'Peter Cullen', 'Brenda Blethyn', 'Kyle Stanger']
9 Capitalism: A Love Story ['Michael Moore', 'Thora Birch', 'William Black', 'Elijah Cummings', 'Baron Hill', 'Marcy Kaptur', 'Wallace Shawn', 'Elizabeth Warren', 'Peter Zalewski']
9 Be Kind Rewind ['Jack Black', 'Yasiin Bey', 'Danny Glover', 'Mia Farrow', 'Marcus Carl Franklin', 'Arjay Smith', 'Paul Dinello', 'Melonie Diaz', 'Sigourney Weaver']
8 Superbabies: Baby Geniuses 2 ['Jon Voight', 'Scott Baio', 'Vanessa Angel', 'Skyler Shaye', 'Whoopi Goldberg', 'Justin Chatwin', 'Peter Wingfield', 'Erik-Michael Estrada']
6 Willard ['Crispin Glover', 'R. Lee Ermey', 'Laura Harring', 'Jackie Burroughs', 'Ashlyn Gere', 'William S. Taylor']
7 Flash of Genius ['Aaron Abrams', 'Alan Alda', 'Lauren Graham', 'Greg Kinnear', 'Tatiana Maslany', 'Tim Kelleher', 'Jake Abel']
9 Bon voyage ['Grégori Derangère', 'Gérard Depardieu', 'Isabelle Adjani', 'Virginie Ledoyen', 'Yvan Attal', 'Peter Coyote', 'Aurore Clément', 'Edith Scob', 'Wolfgang Pissors']
5 Marci X ['Lisa Kudrow', 'Damon Wayans', 'Richard Benjamin', 'Jane Krakowski', 'Christine Baranski']
4 The Children of Huang Shi ['Jonathan Rhys Meyers', 'Radha Mitchell', 'Chow Yun-fat', 'Michelle Yeoh']
7 Steamboy ['Anne Suzuki', 'Masane Tsukayama', 'Katsuo Nakamura', 'Manami Konishi', 'Kiyoshi Kodama', 'Ikki Sawamura', 'Susumu Terajima']
7 The Game of Their Lives ['Gerard Butler', 'Wes Bentley', 'Gavin Rossdale', 'Costas Mandylor', 'Louis Mandylor', 'Zachery Ty Bryan', 'Jimmy Jean-Louis']
6 Three Kingdoms: Resurrection of the Dragon ['Sammo Hung', 'Vanness Wu', 'Maggie Q', 'Andy Lau', 'Ti Lung', 'Elliot Ngok']
8 Dwegons ['Melissa Leo', 'Maggie Wheeler', 'Joey D. Vieira', 'R. Martin Klein', 'Thomas Francis Walsh III', 'Jacqueline Lovell', 'John DeMita', 'Mark Lewis']
6 I Can Do Bad All By Myself ['Tyler Perry', 'Taraji P. Henson', 'Adam Rodríguez', 'Mary J. Blige', 'Gladys Knight', 'Brian J. White']
3 Thomas and the Magic Railroad ['Alec Baldwin', 'Peter Fonda', 'Mara Wilson']
6 The Nutcracker ['Darci Kistler', 'Damian Woetzel', 'Bart Robinson Cook', 'Kyra Nichols', 'Jessica Lynn Cohen', 'Macaulay Culkin']
8 Kansas City ['Jennifer Jason Leigh', 'Miranda Richardson', 'Harry Belafonte', 'Michael Murphy', 'Dermot Mulroney', 'Steve Buscemi', 'Brooke Smith', 'Jane Adams']
6 Out of Inferno ['Lau Ching-Wan', 'Angelica Lee', 'Chen Sicheng', 'Natalie Tong', 'Eddie Cheung Siu-Fai', 'Louis Koo']
7 Young Sherlock Holmes ['Nicholas Rowe', 'Alan Cox', 'Sophie Ward', 'Anthony Higgins', 'Susan Fleetwood', 'Matthew Ryan', 'Earl Rhodes']
8 Fame ['Kay Panabaker', 'Naturi Naughton', 'Kherington Payne', 'Megan Mullally', 'Walter Perez', 'Asher Book', 'Krystal Ellsworth', 'Anna Maria Perez de Tagle']
5 Center Stage ['Amanda Schull', 'Zoe Saldana', 'Susan May Pratt', 'Peter Gallagher', 'Scottie Thompson']
9 Life as a House ['Kevin Kline', 'Kristin Scott Thomas', 'Hayden Christensen', 'Jena Malone', 'Mary Steenburgen', 'Ian Somerhalder', 'Scott Bakula', 'Sandra Nelson', 'Sam Robards']
4 Restoration ["Emily Roya O'Brien", 'Adrian Gaeta', 'Zack Ward', 'Sarah Ann Schultz']
7 Metallica: Through the Never ['Dane DeHaan', 'Mackenzie Gray', 'James Hetfield', 'Lars Ulrich', 'Kirk Hammett', 'Toby Hargrave', 'Robert Trujillo']
6 I Come with the Rain ['Josh Hartnett', 'Elias Koteas', 'Takuya Kimura', 'Lee Byung-hun', 'Tran Nu Yên-Khê', 'Shawn Yue']
8 Wolves ['Jason Momoa', 'Lucas Till', 'John Pyper-Ferguson', 'Stephen McHattie', 'Merritt Patterson', 'Janet-Laine Green', 'Melanie Scrofano', 'Kaitlyn Wong']
9 Black Nativity ['Forest Whitaker', 'Angela Bassett', 'Jennifer Hudson', 'Tyrese Gibson', 'Jacob Latimore', 'Mary J. Blige', 'Nas', 'Vondie Curtis-Hall', 'J. Mallory-McCree']
9 City of Ghosts ['Matt Dillon', 'James Caan', 'Natascha McElhone', 'Gérard Depardieu', 'Stellan Skarsgård', 'Rose Byrne', 'Shawn Andrews', 'Christopher Curry', 'Pok Panhavicyetr']
9 Summer Catch ['Freddie Prinze Jr.', 'Jessica Biel', 'Fred Ward', 'Matthew Lillard', 'Brian Dennehy', 'Jason Gedrick', 'Brittany Murphy', 'Bruce Davison', 'Marc Blucas']
9 A Simple Plan ['Bill Paxton', 'Bridget Fonda', 'Billy Bob Thornton', 'Brent Briscoe', 'Chelcie Ross', 'Gary Cole', 'Becky Ann Baker', 'Tom Carey', 'Jack Walsh']
9 Larry the Cable Guy: Health Inspector ['Larry the Cable Guy', 'Iris Bahr', 'Tony Hale', 'David Koechner', 'Brooke Dillman', 'Joanna Cassidy', 'Megyn Price', 'Tom Hillmann', 'Kristen Wharton']
8 How She Move ['Rutina Wesley', 'Dwain Murphy', 'Boyd Banks', 'Clé Bennett', 'Nina Dobrev', 'Tristan D. Lalla', 'Shawn Desman', "Romina D'Ugo"]
8 Bobby Jones: Stroke of Genius ['Jim Caviezel', 'Claire Forlani', 'Jeremy Northam', 'Malcolm McDowell', 'Aidan Quinn', 'Brett Rice', 'Connie Ray', 'Devon Gearhart']
9 Roar ['Tippi Hedren', 'Melanie Griffith', 'Jerry Marshall', 'Kyalo Mativo', 'Rick Glassey', 'Steve Miller', 'Noel Marshall', 'John Marshall', 'Zakes Mokae']
9 Escobar: Paradise Lost ['Benicio del Toro', 'Josh Hutcherson', 'Brady Corbet', 'Claudia Traisac', 'Carlos Bardem', 'Ana Girardot', 'Tenoch Huerta', 'Laura Londoño', 'Frank Spano']
9 My Girl ['Anna Chlumsky', 'Macaulay Culkin', 'Dan Aykroyd', 'Jamie Lee Curtis', 'Richard Masur', 'Griffin Dunne', 'Peter Michael Goetz', 'Lara Steinick', 'Anny Nelsen']
9 House of Sand and Fog ['Jennifer Connelly', 'Ben Kingsley', 'Ron Eldard', 'Frances Fisher', 'Kim Dickens', 'Shohreh Aghdashloo', 'Jonathan Ahdout', 'Navi Rawat', 'Kia Jam']
9 See Spot Run ['Michael Clarke Duncan', 'David Arquette', 'Leslie Bibb', 'Joe Viterelli', 'Steve Schirripa', 'Anthony Anderson', 'Paul Sorvino', 'Kim Hawthorne', 'Angus T. Jones']
6 The Cookout ['Ja Rule', 'Tim Meadows', 'Jenifer Lewis', 'Jonathan Silverman', 'Eve', 'Kevin Phillips']
6 Duets ['Gwyneth Paltrow', 'Scott Speedman', 'Maria Bello', 'Paul Giamatti', 'Andre Braugher', 'Huey Lewis']
9 The Immigrant ['Marion Cotillard', 'Jeremy Renner', 'Joaquin Phoenix', 'Dagmara Domińczyk', 'Gabriel Rush', 'Antoni Corone', 'Deedee Luxe', 'Angela Sarafyan', "Sofia Black-D'Elia"]
5 Good ['Viggo Mortensen', 'Jason Isaacs', 'Mark Strong', 'Steven Mackintosh', 'Jodie Whittaker']
8 Enter the Void ['Nathaniel Brown', 'Paz de la Huerta', 'Cyril Roy', 'Masato Tanno', 'Jesse Kuhn', 'Ed Spear', 'Emily Alyn Lind', 'Olly Alexander']
5 Slow Burn ['Ray Liotta', 'LL Cool J', 'Mekhi Phifer', 'Jolene Blalock', 'Chiwetel Ejiofor']
8 Three Men and a Baby ['Tom Selleck', 'Steve Guttenberg', 'Ted Danson', 'Nancy Travis', 'Margaret Colin', 'Camilla Scott', 'Philip Bosco', 'Colin Quinn']
5 The Yellow Handkerchief ['William Hurt', 'Maria Bello', 'Kristen Stewart', 'Eddie Redmayne', 'Veronica Russell']
8 Private Benjamin ['Goldie Hawn', 'Eileen Brennan', 'Armand Assante', 'Robert Webber', 'Mary Kay Place', 'Harry Dean Stanton', 'Albert Brooks', 'Kopi Sotiropulos']
7 Mama ['Jessica Chastain', 'Nikolaj Coster-Waldau', 'Megan Charpentier', 'Isabelle Nélisse', 'Daniel Kash', 'Melina Matthews', 'Morgan McGarry']
9 Bad Grandpa ['Johnny Knoxville', 'Jackson Nicoll', 'Georgina Cates', 'Spike Jonze', 'Catherine Keener', 'Kamber Hejlik', 'Jack Polick', 'Grasie Mercedes', 'Zia Harris']
9 Why Did I Get Married? ['Tyler Perry', 'Jill Scott', 'Janet Jackson', 'Michael Jai White', 'Malik Yoba', 'Sharon Leal', 'Richard T. Jones', 'Tasha Smith', 'Kaira Akita']
8 Confessions of a Teenage Drama Queen ['Lindsay Lohan', 'Adam Garcia', 'Glenne Headly', 'Alison Pill', 'Megan Fox', 'Barbara Mamabolo', 'Pedro Miguel Arce', 'Jessica Barrera']
5 Book of Shadows: Blair Witch 2 ['Kim Director', 'Jeffrey Donovan', 'Erica Leerhsen', 'Tristine Skyler', 'Stephen Barker Turner']
8 Flicka ['Tim McGraw', 'Maria Bello', 'Armie Hammer', 'Alison Lohman', 'Ryan Kwanten', 'Danny Pino', 'Dallas Roberts', 'Kaylee DeFer']
8 Tuck Everlasting ['Alexis Bledel', 'William Hurt', 'Sissy Spacek', 'Jonathan Jackson', 'Scott Bairstow', 'Ben Kingsley', 'Amy Irving', 'Victor Garber']
7 Country Strong ['Gwyneth Paltrow', 'Garrett Hedlund', 'Tim McGraw', 'Leighton Meester', 'Marshall Chapman', 'Lari White', 'Jeremy Childs']
4 U2 3D ['Bono', 'The Edge', 'Adam Clayton', ' Larry Mullen Jr.']
6 Highlander: Endgame ['Christopher Lambert', 'Bruce Payne', 'Adrian Paul', 'Donnie Yen', 'Lisa Barbuscia', 'Beatie Edney']
0 Barney's Great Adventure []
8 Home Fries ['Drew Barrymore', "Catherine O'Hara", 'Luke Wilson', 'Jake Busey', 'Shelley Duvall', 'Kim Robillard', 'Daryl Mitchell', 'Chris Ellis']
8 Here On Earth ['Leelee Sobieski', 'Chris Klein', 'Josh Hartnett', 'Michael Rooker', 'Annie Corley', 'Bruce Greenwood', "Annette O'Toole", 'Elaine Hendrix']
4 The Love Letter ['Campbell Scott', 'Jennifer Jason Leigh', 'David Dukes', 'Estelle Parsons']
9 The Clan of the Cave Bear ['Daryl Hannah', 'Pamela Reed', 'James Remar', 'Thomas G. Waites', 'John Doolittle', 'Curtis Armstrong', 'Martin Doyle', 'Nicole Eggert', 'Salome Jens']
6 Listening ['Thomas Stroppel', 'Artie Ahr', 'Amber Marie Bollinger', 'Christine Haeberman', 'Steve Hanks', 'Buddy Daniels']
4 Ong Bak 2 ['Tony Jaa', 'Sarunyu Wongkrachang', 'Sorapong Chatree', 'Primorata Dejudom']
4 Silent Trigger ['Dolph Lundgren', 'Gina Bellman', 'Conrad Dunn', 'Christopher Heyerdahl']
9 All The Queen's Men ['Matt LeBlanc', 'Eddie Izzard', 'James Cosmo', 'Nicolette Krebitz', 'David Tristan Birkin', 'Edward Fox', 'Udo Kier', 'Oliver Korittke', 'Karl Markovics']
7 Dungeons & Dragons: Wrath of the Dragon God ['Bruce Payne', 'Mark Dymond', 'Clemency Burton-Hill', 'Ellie Chidzey', 'Tim Stern', 'Lucy Gaskell', 'Leonardas Pobedonoscevas']
7 All About the Benjamins ['Ice Cube', 'Mike Epps', 'Tommy Flanagan', 'Carmen Chaplin', 'Eva Mendes', 'Roger Guenveur Smith', 'Oscar Isaac']
9 Vampire in Brooklyn ['Eddie Murphy', 'Angela Bassett', 'Allen Payne', 'Kadeem Hardison', 'John Witherspoon', 'Zakes Mokae', 'Joanna Cassidy', 'W. Earl Brown', 'Simbi Khali']
9 New York, New York ['Liza Minnelli', 'Robert De Niro', 'Lionel Stander', 'Barry Primus', 'Dick Miller', 'Mary Kay Place', 'Shera Danese', 'Frank Sivero', 'Don Calfa']
9 Gossip ['Joshua Jackson', 'James Marsden', 'Kate Hudson', 'Lena Headey', 'Norman Reedus', 'Eric Bogosian', 'Edward James Olmos', 'Sharon Lawrence', 'Marisa Coughlan']
9 Caravans ['Anthony Quinn', "Jennifer O'Neill", 'Michael Sarrazin', 'Christopher Lee', 'Joseph Cotten', 'Barry Sullivan', 'Behrouz Vossoughi', 'Jeremy Kemp', 'Duncan Quinn']
6 The Caveman's Valentine ['Samuel L. Jackson', 'Colm Feore', 'Ann Magnuson', 'Aunjanue Ellis', 'Tamara Tunie', 'Anthony Michael Hall']
5 Justin Bieber: Never Say Never ['Justin Bieber', 'Miley Cyrus', 'Usher Raymond', 'Jaden Smith', 'Sean Kingston']
7 This Christmas ['Loretta Devine', 'Delroy Lindo', 'Idris Elba', 'Regina King', 'Laz Alonso', 'Lauren London', 'Chris Brown']
6 Baby Geniuses ['Kathleen Turner', 'Christopher Lloyd', 'Kim Cattrall', 'Peter MacNicol', 'Dom DeLuise', 'Dan Monahan']
7 Harriet the Spy ['Michelle Trachtenberg', "Rosie O'Donnell", 'J. Smith-Cameron', 'Eartha Kitt', 'Vanessa Lee Chester', 'Gregory Smith', 'Robert Joy']
9 Resurrecting the Champ ['Samuel L. Jackson', 'Josh Hartnett', 'Alan Alda', 'Teri Hatcher', 'Kathryn Morris', 'Dakota Goyo', 'Rachel Nichols', 'Nick Sandow', 'Kristen Shaw']
7 Excessive Force ['Thomas Ian Griffith', 'Lance Henriksen', 'James Earl Jones', 'Burt Young', 'Tony Todd', 'Antoni Corone', 'Charlotte Lewis']
7 The Claim ['Peter Mullan', 'Milla Jovovich', 'Wes Bentley', 'Nastassja Kinski', 'Sarah Polley', 'Shirley Henderson', 'Julian Richings']
9 The Vatican Tapes ['Olivia Taylor Dudley', 'Michael Peña', 'Djimon Hounsou', 'Dougray Scott', 'Peter Andersson', 'Kathleen Robertson', 'John Patrick Amedori', 'Cas Anvar', 'Michael Paré']
9 The Emperor's Club ['Kevin Kline', 'Emile Hirsch', 'Embeth Davidtz', 'Rob Morrow', 'Edward Herrmann', 'Helen Carey', 'Jesse Eisenberg', 'Paul Dano', "Katherine O'Sullivan"]
9 The Killer Inside Me ['Casey Affleck', 'Kate Hudson', 'Jessica Alba', 'Ned Beatty', 'Tom Bower', 'Simon Baker', 'Bill Pullman', 'Elias Koteas', 'Liam Aiken']
6 Oscar and Lucinda ['Ralph Fiennes', 'Cate Blanchett', 'Ciarán Hinds', 'Tom Wilkinson', 'Richard Roxburgh', 'Christian Manon']
8 The Land Before Time ['Gabriel Damon', 'Candace Hutson', 'Judith Barsi', 'Will Ryan', 'Pat Hingle', 'Helen Shaver', 'Bill Erwin', 'Burke Byrnes']
8 The Golden Child ['Eddie Murphy', 'Charles Dance', 'Charlotte Lewis', 'Victor Wong', 'Peter Kwong', 'Jasmine Reate', 'James Hong', "Randall 'Tex' Cobb"]
9 Chronicle ['Dane DeHaan', 'Alex Russell', 'Michael B. Jordan', 'Michael Kelly', 'Anna Wood', 'Ashley Hinshaw', 'Joe Vaz', 'Luke Tyler', 'Crystal-Donna Roberts']
7 Yentl ['Barbra Streisand', 'Mandy Patinkin', 'Amy Irving', 'Nehemiah Persoff', 'Steven Hill', 'Miriam Margolyes', 'Jonathan Tafler']
9 Crossroads ['Britney Spears', 'Zoe Saldana', 'Taryn Manning', 'Anson Mount', 'Dan Aykroyd', 'Justin Long', 'Jamie Lynn Spears', 'Kim Cattrall', 'Seth Romatelli']
6 My Baby's Daddy ['Eddie Griffin', 'Anthony Anderson', 'Michael Imperioli', 'Method Man', 'Paula Jai Parker', 'Bai Ling']
4 Def Jam's How to Be a Player ['Bill Bellamy', 'Lark Voorhies', 'Bernie Mac', 'Elise Neal']
8 Living Out Loud ['Holly Hunter', 'Danny DeVito', 'Queen Latifah', 'Martin Donovan', 'Rachael Leigh Cook', 'Richard Schiff', 'Elias Koteas', 'Suzanne Shepherd']
9 Sorority Boys ['Barry Watson', 'Michael Rosenbaum', 'Harland Williams', 'Melissa Sagemiller', 'Tony Denman', 'Brad Beyer', 'Kathryn Stockwood', 'Heather Matarazzo', 'Lydia Hull']
7 Screwed ['Norm Macdonald', 'Dave Chappelle', 'Danny DeVito', 'Elaine Stritch', 'Daniel Benzali', 'Sherman Hemsley', 'Sarah Silverman']
6 In the Cut ['Meg Ryan', 'Mark Ruffalo', 'Jennifer Jason Leigh', 'Nick Damici', 'Heather Litteer', 'Kevin Bacon']
8 The Pursuit of D.B. Cooper ['Robert Duvall', 'Treat Williams', 'Kathryn Harrold', 'Ed Flanders', 'Paul Gleason', 'R. G. Armstrong', 'Dorothy Fielding', 'Howard K. Smith']
7 The Dangerous Lives of Altar Boys ['Emile Hirsch', 'Kieran Culkin', 'Jodie Foster', "Vincent D'Onofrio", 'Jena Malone', 'Jake Richardson', 'Melissa McBride']
9 Duma ['Alex Michaeletos', 'Campbell Scott', 'Mary Makhatho', 'Nthabiseng Kenoshi', 'Hope Davis', 'Jennifer Steyn', 'Nicky Rebello', 'Javad Ramezani', 'Eamonn Walker']
7 The Life Before Her Eyes ['Uma Thurman', 'Evan Rachel Wood', 'Eva Amurri Martino', 'Gabrielle Brennan', 'Brett Cullen', 'Oscar Isaac', 'Jack Gilpin']
9 Darling Companion ['Diane Keaton', 'Kevin Kline', 'Sam Shepard', 'Dianne Wiest', 'Richard Jenkins', 'Elisabeth Moss', 'Mark Duplass', 'Ayelet Zurer', 'Jay Ali']
5 A Woman, a Gun and a Noodle Shop ['Sun Honglei', 'Xiao Shen Yang', 'Yan Ni', 'Ni Dahong', 'Zhao Benshan']
5 City of Life and Death ['Liu Ye', 'Gao Yuanyuan', 'Hideo Nakaizumi', 'John Paisley', 'Beverly Peckous']
5 Legend of a Rabbit ['Jon Heder', 'Tom Arnold', 'Michael Clarke Duncan', 'Rebecca Black', 'Claire Geare']
9 Triangle ['Melissa George', 'Liam Hemsworth', 'Emma Lung', 'Rachael Carpani', 'Michael Dorman', 'Joshua McIvor', 'Henry Nixon', 'Jack Taylor', 'Bryan Probets']
8 Dancin' It's On ['Witney Carson', 'Chehon Wespi-Tschopp', 'Gary Daniels', 'David Winters', 'Jordan Clark', 'Matt Marr', 'Russell Ferguson', 'Ava Fabian']
4 A Tale of Three Cities ['Lau Ching-Wan', 'Tang Wei', 'Qin Hailu', 'Jing Boran ']
9 Phone Booth ['Colin Farrell', 'Kiefer Sutherland', 'Forest Whitaker', 'Radha Mitchell', 'Katie Holmes', 'Paula Jai Parker', 'Domenick Lombardozzi', 'James MacDonald', 'Ben Foster']
9 Tomcats ["Jerry O'Connell", 'Shannon Elizabeth', 'Jake Busey', 'Horatio Sanz', 'Bernie Casey', 'Jaime Pressly', 'David Ogden Stiers', 'Bill Maher', 'Dakota Fanning']
7 The Perez Family ['Marisa Tomei', 'Alfred Molina', 'Anjelica Huston', 'Chazz Palminteri', 'Trini Alvarado', 'Ruben Rabasa', 'Luis Raúl']
9 The Molly Maguires ['Sean Connery', 'Samantha Eggar', 'Richard Harris', 'Frank Finlay', 'Anthony Zerbe', 'Bethel Leslie', 'Art Lund', 'Philip Bourneuf', 'Ian Abercrombie']
9 Copying Beethoven ['Ed Harris', 'Diane Kruger', 'Matthew Goode', 'Phyllida Law', 'Ralph Riach', 'Bill Stewart', 'Angus Barnett', 'Viktoria Dihen', 'Matyelok Gibbs']
6 An Ideal Husband ['Cate Blanchett', 'Minnie Driver', 'Rupert Everett', 'Julianne Moore', 'Jeremy Northam', 'Peter Vaughan']
7 Darkness ['Anna Paquin', 'Lena Olin', 'Iain Glen', 'Giancarlo Giannini', 'Fele Martínez', 'Stephan Enquist', 'Fermí Reixach']
6 The Blue Butterfly ['Marc Donato', 'Pascale Bussières', 'William Hurt', 'Raoul Max Trujillo', 'Steve Adams', 'Marianella Jimenez']
9 There Goes My Baby ['Dermot Mulroney', 'Ricky Schroder', 'Kelli Williams', 'Noah Wyle', 'Lucy Deakins', 'Jill Schoelen', 'Kristin Minter', 'Kenneth Ransom', 'Seymour Cassel']
5 For Greater Glory - The True Story of Cristiada ['Eva Longoria', 'Andy García', 'Oscar Isaac', "Peter O'Toole", 'Rubén Blades']
8 Misconduct ['Josh Duhamel', 'Alice Eve', 'Malin Åkerman', 'Lee Byung-hun', 'Julia Stiles', 'Glen Powell', 'Al Pacino', 'Anthony Hopkins']
8 The Banger Sisters ['Goldie Hawn', 'Susan Sarandon', 'Geoffrey Rush', 'Erika Christensen', 'Robin Thomas', 'Eva Amurri Martino', 'Matthew Carey', 'Andre Ware']
7 Kung Pow: Enter the Fist ['Hui Lou Chen', 'Tad Horino', 'Steve Oedekerk', 'Jennifer Tung', 'Ming Lo', 'Peggy Lu', 'Liu Chia-Liang']
7 One Direction: This Is Us ['Harry Styles', 'Niall Horan', 'Zayn Malik', 'Louis Tomlinson', 'Liam Payne', 'Jon Shone', 'Dan Richards']
8 Hey Arnold! The Movie ['Spencer Klein', 'Francesca Smith', 'Jamil Walker Smith', 'Dan Castellaneta', 'Tress MacNeille', 'Paul Sorvino', 'Jennifer Jason Leigh', 'Christopher Lloyd']
6 Love Jones ['Larenz Tate', 'Nia Long', 'Isaiah Washington', 'Bill Bellamy', 'Lisa Nicole Carson', 'Marie-Françoise Theodore']
5 End of the Spear ['Louie Leonardo', 'Chad Allen', 'Jack Guzman', 'Chase Ellison', 'Sylvia Jefferies']
9 Danny Collins ['Al Pacino', 'Annette Bening', 'Jennifer Garner', 'Bobby Cannavale', 'Christopher Plummer', 'Josh Peck', 'Katarina Cas', 'Nick Offerman', 'Melissa Benoist']
8 Malone ['Burt Reynolds', 'Cliff Robertson', 'Kenneth McMillan', 'Cynthia Gibb', 'Scott Wilson', 'Lauren Hutton', 'Dennis Burkley', 'Tracey Walter']
8 Peaceful Warrior ['Scott Mechlowicz', 'Nick Nolte', 'Amy Smart', 'Tim DeKay', 'Ashton Holmes', 'Paul Wesley', 'Agnes Bruckner', 'B.J. Britt']
6 Swept Away ['Madonna', 'Adriano Giannini', 'Bruce Greenwood', 'Elizabeth Banks', 'Michael Beattie', 'Jeanne Tripplehorn']
6 The Brown Bunny ['Vincent Gallo', 'Chloë Sevigny', 'Cheryl Tiegs', 'Elizabeth Blake', 'Anna Vareschi', 'Mary Morasky']
4 The Swindle ['Michel Serrault', 'Isabelle Huppert', 'François Cluzet', 'Jean-François Balmer']
4 The Chambermaid on the Titanic ['Olivier Martinez', 'Aitana Sánchez-Gijón', 'Romane Bohringer', 'Didier Bezace']
9 Imaginary Heroes ['Sigourney Weaver', 'Ryan Donowho', 'Emile Hirsch', 'Jeff Daniels', 'Michelle Williams', "Deirdre O'Connell", 'Kip Pardue', 'Jay Paulson', 'Terry Beaver']
9 Blood Done Sign My Name ['Natalie Alyn Lind', 'Michael Rooker', 'Emily Alyn Lind', 'Omar Benson Miller', 'Lee Norris', 'Nate Parker', 'Ricky Schroder', 'Lela Rochon', 'Gattlin Griffith']
8 The Open Road ['Justin Timberlake', 'Jeff Bridges', 'Kate Mara', 'Harry Dean Stanton', 'Mary Steenburgen', 'Bret Saberhagen', 'Allen O. Battle III', 'James Harlon Palmer']
3 Free Style ['Corbin Bleu', 'Sandra Echeverría', 'Madison Pettis']
8 Blonde Ambition ['Jessica Simpson', 'Luke Wilson', 'Rachael Leigh Cook', 'Penelope Ann Miller', 'Andy Dick', 'Larry Miller', 'Willie Nelson', 'Penny Marshall']
5 The Reef ['Adrienne Pickering', 'Zoe Naylor', 'Gyton Grantley', 'Damian Walshe-Howling', 'Kieran Darcy-Smith']
9 White Noise 2: The Light ['Nathan Fillion', 'Katee Sackhoff', 'Craig Fairbrass', 'Adrian Holmes', 'Teryl Rothery', 'William MacDonald', 'Joshua Ballard', 'David Milchard', 'Cory Monteith']
7 Beat the World ['Tyrone Brown', 'Mishael Morgan', 'Nikki Grant', 'Chase Armitage', 'Ray Johnson', 'Kristy Flores', 'Shane Pollard']
6 Jungle Shuffle ['Drake Bell', 'Rob Schneider', 'Brianne Siddall', "Joey D'Auria", 'Jessica DiCicco', 'Chris Gardner']
9 Adam Resurrected ['Jeff Goldblum', 'Willem Dafoe', 'Derek Jacobi', 'Ayelet Zurer', 'Hana Laslo', 'Joachim Król', 'Jenya Dodina', 'Idan Alterman', 'Juliane Köhler']
8 Partition ['Kristin Kreuk', 'Jimi Mistry', 'Neve Campbell', 'John Light', 'Irrfan Khan', 'Madhur Jaffrey', 'Chenier Hundal', 'Jesse Moss']
3 Good Intentions ['Luke Perry', 'LeAnn Rimes', 'Jimmi Simpson']
8 Plastic ['Ed Speleers', 'Will Poulter', 'Alfie Allen', 'Sebastian de Souza', 'Emma Rigby', 'Thomas Kretschmann', 'Graham McTavish', 'Malese Jow']
8 Poltergeist III ['Tom Skerritt', 'Nancy Allen', "Heather O'Rourke", 'Lara Flynn Boyle', 'Kipley Wentz', 'Zelda Rubinstein', 'Richard Fire', 'Nathan Davis']
9 Gentlemen Broncos ['Michael Angarano', 'Sam Rockwell', 'Clive Revill', 'Jemaine Clement', 'Jennifer Coolidge', 'Héctor Jiménez', 'Suzanne May', 'Halley Feiffer', 'Steve Berg']
8 The Best Man ['Nia Long', 'Morris Chestnut', 'Harold Perrineau', 'Terrence Howard', 'Sanaa Lathan', 'Taye Diggs', 'Regina Hall', 'Monica Calhoun']
6 Child's Play ['Catherine Hicks', 'Chris Sarandon', 'Alex Vincent', 'Brad Dourif', 'Dinah Manoff', 'Ed Gale']
6 Sicko ['Michael Moore', 'George W. Bush', 'Bill Clinton', 'Hillary Clinton', 'Billy Crystal', 'Tony Benn']
7 Breakin' All the Rules ['Jamie Foxx', 'Morris Chestnut', 'Jennifer Esposito', 'Gabrielle Union', 'Peter MacNicol', 'Heather Headley', 'Octavia Spencer']
9 Chasing Papi ['Roselyn Sánchez', 'Sofía Vergara', 'Jaci Velasquez', 'Eduardo Verástegui', 'Lisa Vidal', 'Freddy Rodríguez', 'María Conchita Alonso', 'D. L. Hughley', 'Germán Legarreta']
6 The Legend of Suriyothai ['M.L. Piyapas Bhirombhakdi', 'Sarunyu Wongkrachang', 'Chatchai Plengpanich', 'Johnny Anfone', 'Mai Charoenpura', 'Sinjai Plengpanit']
5 Princess Kaiulani ["Q'orianka Kilcher", 'Barry Pepper', 'Will Patton', 'Jimmy Yuill', 'Shaun Evans']
8 Opal Dream ['Sapphire Boyce', 'Christian Byers', 'Vince Colosimo', 'Jacqueline McKenzie', 'Robert Morgan', 'Anna Linarello', 'Denise Roberts', 'Peter Callan']
7 The Girl on the Train ['Michel Blanc', 'Catherine Deneuve', 'Émilie Dequenne', 'Nicolas Duvauchelle', 'Mathieu Demy', 'Ronit Elkabetz', 'Jérémie Quaegebeur']
9 Ultramarines: A Warhammer 40,000 Movie ['Terence Stamp', 'John Hurt', 'Sean Pertwee', 'Steven Waddington', 'Donald Sumpter', 'Johnny Harris', 'Ben Bishop', 'Christopher Finney', 'Gary Martin']
9 Crazy Heart ['Jeff Bridges', 'Maggie Gyllenhaal', 'Colin Farrell', 'Robert Duvall', 'Paul Herman', 'Tom Bower', 'Brian Gleason', 'J. Michael Oliva', 'Beth Grant']
9 The Namesake ['Kal Penn', 'Tabu', 'Irrfan Khan', 'Sahira Nair', 'Jacinda Barrett', 'Zuleikha Robinson', 'Ruma Guha Thakurta', 'Sabyasachi Chakraborty', 'Supriya Choudhury']
9 Glitter ['Mariah Carey', 'Max Beesley', 'Terrence Howard', 'Valarie Pettiford', 'Padma Lakshmi', 'Tia Texada', 'Da Brat', 'Eric Benet', 'Don Ackerman']
7 The Haunting in Connecticut 2: Ghosts of Georgia ['Chad Michael Murray', 'Katee Sackhoff', 'Abigail Spencer', 'Cicely Tyson', 'Emily Alyn Lind', 'Andrea Frankle', 'Lauren Pennington']
8 Silmido ['Sol Kyung-gu', 'Heo Jun-ho', 'Ahn Sung-Ki', 'Jung Jae-young', 'Im Won-hee', 'Kang Shin-il', 'Ji-Hwan Jo', 'Kang Seong-jin']
1 All Is Lost ['Robert Redford']
4 Limbo ['Mary Elizabeth Mastrantonio', 'David Strathairn', 'Vanessa Martinez', 'Kris Kristofferson']
6 Yeh Jawaani Hai Deewani ['Ranbir Kapoor', 'Deepika Padukone', 'Kalki Koechlin', 'Aditya Roy Kapoor', 'Kunaal Roy Kapur', 'Evelyn Sharma']
6 Valley of the Wolves: Iraq ['Muhammed Necati Şaşmaz', 'Billy Zane', 'Ghassan Massoud', 'Gurkan Uygun', 'Bergüzar Korel', 'Gary Busey']
6 You Got Served ['Marques Houston', 'Omarion', 'J-Boog', "Lil' Fizz", 'Raz B', 'Jennifer Freeman']
5 A Thin Line Between Love and Hate ['Lynn Whitfield', 'Martin Lawrence', 'Regina King', 'Della Reese', 'Bobby Brown']
9 The Inkwell ['Larenz Tate', 'Joe Morton', 'Suzzanne Douglas', 'Glynn Turman', 'Vanessa Bell Calloway', 'A.J. Johnson', 'Morris Chestnut', 'Jada Pinkett Smith', 'Duane Martin']
7 Woman on Top ['Penélope Cruz', 'Murilo Benicio', 'Mark Feuerstein', 'John de Lancie', 'Anne Ramsay', 'Ana Gasteyer', 'Harold Perrineau']
3 Anomalisa ['David Thewlis', 'Jennifer Jason Leigh', 'Tom Noonan']
9 8 Women ['Catherine Deneuve', 'Isabelle Huppert', 'Emmanuelle Béart', 'Fanny Ardant', 'Virginie Ledoyen', 'Ludivine Sagnier', 'Firmine Richard', 'Danielle Darrieux', 'Dominique Lamure']
8 Clay Pigeons ['Joaquin Phoenix', 'Vince Vaughn', 'Janeane Garofalo', 'Gregory Sporleder', 'Georgina Cates', 'Vince Vieluf', 'Joseph D. Reitman', 'Nicole Arlyn']
7 Prefontaine ['Jared Leto', 'R. Lee Ermey', "Ed O'Neill", 'Breckin Meyer', 'Lindsay Crouse', 'Amy Locane', 'Laurel Holloman']
8 The Secret of Kells ['Evan McGuire', 'Christen Mooney', 'Brendan Gleeson', 'Mick Lally', 'Liam Hourican', 'Paul Tylak', 'Michael McGrath', 'Paul Young']
5 The Land Girls ['Catherine McCormack', 'Rachel Weisz', 'Anna Friel', 'Paul Bettany', 'Steven Mackintosh']
7 Pathology ['Milo Ventimiglia', 'Alyssa Milano', 'Michael Weston', 'Lauren Lee Smith', 'Johnny Whitworth', 'John de Lancie', 'Meiling Melançon']
8 Dear Wendy ['Jamie Bell', 'Bill Pullman', 'Michael Angarano', 'Danso Gordon', 'Alison Pill', 'Chris Owen', 'Mark Webber', 'Novella Nelson']
8 The Rocket: The Legend of Rocket Richard ['Roy Dupuis', 'Michel Barrette', 'Rémy Girard', 'Tony Calabretta', 'Sean Avery', 'Philip Craig', 'Paul Doucet', 'Pascal Dupuis']
8 Swelter ['Jean-Claude Van Damme', 'Brad Carter', 'Josh Henderson', 'Alfred Molina', 'Lennie James', 'Freya Tingley', 'Grant Bowler', 'Catalina Sandino Moreno']
9 Rumble in the Bronx ['Jackie Chan', 'Anita Mui', 'Françoise Yip', 'Bill Tung', 'Marc Akerstream', 'Garvin Cross', 'Morgan Lam', 'Kris Lord', 'Carrie Cain-Sparks']
9 The Hotel New Hampshire ['Rob Lowe', 'Jodie Foster', 'Paul McCrane', 'Beau Bridges', 'Seth Green', 'Nastassja Kinski', 'Joely Richardson', 'Wallace Shawn', 'Fred Döderlein']
8 Witless Protection ['Larry the Cable Guy', 'Ivana Miličević', 'Jenny McCarthy', 'Yaphet Kotto', 'Peter Stormare', 'Eric Roberts', 'Joe Mantegna', 'Kurt Naebig']
7 The Work and the Glory ['Sam Hennings', 'Brenda Strong', 'Eric Johnson', 'Alexander Carroll', 'Tiffany Dupont', 'Colin Ford', 'Edward Albert']
5 The Omega Code ['Casper Van Dien', 'Michael York', 'Catherine Oxenberg', 'Michael Ironside', 'Jan Tříska']
8 Pound of Flesh ['Jean-Claude Van Damme', 'John Ralston', 'Darren Shahlavi', 'Aki Aleong', 'Jason Tobin', 'Charlotte Peters', 'Andrew Ng', 'Mike Leeder']
6 My Dog Skip ['Frankie Muniz', 'Diane Lane', 'Kevin Bacon', 'Luke Wilson', 'Chaon Cross', 'Harry Connick Jr.']
8 Michael Jordan to the Max ['Michael Jordan', 'Phil Jackson', 'Bob Costas', 'Bill Murray', 'Laurence Fishburne', 'Ken Griffey, Jr.', 'Spike Lee', 'Steve Kerr']
7 Alien Zone ['John Ericson', 'Ivor Francis', 'Judith Novgrod', 'Burr DeBenning', 'Charles Aidman', 'Bernard Fox', 'Richard Gates']
8 Get Low ['Bill Murray', 'Sissy Spacek', 'Robert Duvall', 'Lucas Black', 'Bill Cobbs', 'Gerald McRaney', 'Scott Cooper', 'Chandler Riggs']
4 The Other Side of Heaven ['Christopher Gorham', 'Anne Hathaway', 'Joe Folau', 'Miriama Smith']
9 A Dog Of Flanders ['Jack Warden', 'Jeremy James Kissner', 'Jesse James', 'Jon Voight', 'Cheryl Ladd', 'Bruce McGill', 'Steven Hartley', 'Andrew Bicknell', 'Farren Monet']
5 The Mighty Macs ['Carla Gugino', 'Ellen Burstyn', 'Marley Shelton', 'David Boreanaz', 'Jennifer Butler']
9 I Hope They Serve Beer in Hell ['Matt Czuchry', 'Jesse Bradford', 'Marika Dominczyk', 'Traci Lords', 'Geoff Stults', 'Keri Lynn Pratt', 'Meagen Fay', 'Susie Abromeit', 'Tricia Munford']
9 Chairman of the Board ["Scott 'Carrot Top' Thompson", 'Courtney Thorne-Smith', 'Larry Miller', 'Jack Warden', 'M. Emmet Walsh', 'Jack McGee', 'Taylor Negron', 'Raquel Welch', 'Fred Stoller']
2 Gerry ['Casey Affleck', 'Matt Damon']
8 Hard to Be a God ['Leonid Yarmolnik', 'Yuriy Tsurilo', 'Natalya Moteva', 'Aleksandr Chutko', 'Aleksandr Ilin', 'Evgeniy Gerchakov', 'Pyotr Merkuryev', 'Juris Laucinsh']
5 The Snow Queen ['Ivan Okhlobystin', 'Dmitriy Nagiev', 'Lyudmila Artemeva', 'Anna Ardova', 'Elizaveta Arzamasova']
5 Alpha and Omega: The Legend of the Saw Tooth Cave ['Dee Dee Greene', 'Ben Diskin', 'Lindsay Torrance', 'Kate Higgins', 'Christopher Corey Smith']
5 Bran Nue Dae ['Rocky McKenzie', 'Geoffrey Rush', 'Jessica Mauboy', 'Ernie Dingo', 'Missy Higgins']
7 The Four Seasons ['Alan Alda', 'Carol Burnett', 'Len Cariou', 'Sandy Dennis', 'Rita Moreno', 'Jack Weston', 'Bess Armstrong']
7 The Adventures of Huck Finn ['Elijah Wood', 'Courtney B. Vance', 'Robbie Coltrane', 'Jason Robards', 'Ron Perlman', 'Dana Ivey', 'Anne Heche']
8 The Work and the Glory II: American Zion ['Sam Hennings', 'Brenda Strong', 'Eric Johnson', 'Alexander Carroll', 'Brighton Hertford', 'Kimberly Varadi', 'Colin Ford', 'Emily Podleski']
9 A Home at the End of the World ['Colin Farrell', 'Dallas Roberts', 'Robin Wright', 'Sissy Spacek', 'Ryan Donowho', 'Erik Smith', 'Harris Allan', 'Andrew Chalmers', 'Ron Lea']
8 Tracker ['Ray Winstone', 'Temuera Morrison', 'Andy Anderson', 'Gareth Reeves', 'Mark Mitchinson', 'Daniel Musgrove', 'Tim McLachlan', 'Jed Brophy']
8 The Brothers ['Morris Chestnut', 'D. L. Hughley', 'Bill Bellamy', 'Shemar Moore', 'Tatyana Ali', 'Jenifer Lewis', 'Tamala Jones', 'Gabrielle Union']
6 Daddy Day Camp ['Cuba Gooding Jr.', 'Tamala Jones', 'Paul Rae', 'Lochlyn Munro', 'Richard Gant', 'Talon G. Ackerman']
8 Mystic Pizza ['Annabeth Gish', 'Julia Roberts', 'Lili Taylor', "Vincent D'Onofrio", 'William R. Moses', 'Adam Storke', 'Matt Damon', 'Conchata Ferrell']
2 Dolphins and Whales: Tribes of the Ocean ['Daryl Hannah', 'Charlotte Rampling']
8 Only the Strong ['Mark Dacascos', 'Geoffrey Lewis', 'Stacey Travis', 'Paco Christian Prieto', 'Todd Susman', 'Jeffrey Anderson-Gunter', 'Richard Coca', 'Frank Dux']
9 Goddess of Love ['Alexis Kendra', 'Elizabeth Sandy', 'Monda Scott', 'Woody Naismith', 'Ray Grady', 'Richard Velton', 'Hugh Westbourne', 'Rachel Alig', 'Deana Ricks']
5 The Business of Strangers ['Julia Stiles', 'Stockard Channing', 'Frederick Weller', 'Marcus Giamatti', 'Jack Hallett']
5 The Flower of Evil ['Benoît Magimel', 'Mélanie Doutey', 'Suzanne Flon', 'Bernard Le Coq', 'Nathalie Baye']
8 Surfer, Dude ['Matthew McConaughey', 'Jeffrey Nordling', 'Willie Nelson', 'Woody Harrelson', 'Zachary Knighton', 'Ramón Rodríguez', 'Travis Fimmel', 'Amber Hay']
3 Lake of Fire ['Noam Chomsky', 'Bill Baird', 'Flip Benham']
5 Men of War ['Dolph Lundgren', 'Charlotte Lewis', 'BD Wong', 'Tim Guinee', 'Catherine Bell']
7 Don McKay ['Thomas Haden Church', 'Elisabeth Shue', 'Melissa Leo', 'M. Emmet Walsh', 'Keith David', 'James Rebhorn', 'Pruitt Taylor Vince']
6 A Shine of Rainbows ['Connie Nielsen', 'Aidan Quinn', 'John Bell', 'Tara Alice Scully', 'Niamh Shaw', 'Jack Gleeson']
5 Song One ['Anne Hathaway', 'Johnny Flynn', 'Mary Steenburgen', 'Ben Rosenfield', 'Lola Kirke']
7 Trade Of Innocents ['Dermot Mulroney', 'Mira Sorvino', 'John Billingsley', 'Trieu Tran', 'Kiều Chinh', 'Tanapol Chuksrida', 'Vithaya Pansringarm']
6 Khiladi 786 ['Akshay Kumar', 'Asin Thottumkal', 'Himesh Reshammiya', 'Mithun Chakraborty', 'Raj Babbar', 'Johnny Lever']
9 Le Havre ['André Wilms', 'Kati Outinen', 'Blondin Miguel', 'Elina Salo', 'Evelyne Didi', 'Quoc Dung Nguyen', 'Jean-Pierre Darroussin', 'Jean-Pierre Léaud', 'Pierre Étaix']
9 Rang De Basanti ['Aamir Khan', 'Soha Ali Khan', 'Alice Patten', 'Sharman Joshi', 'Kunal Kapoor', 'Atul Kulkarni', 'Madhavan', 'Siddharth', 'Kirron Kher']
6 Animals ['David Dastmalchian', 'Kim Shaw', 'John Heard', 'John Hoogenakker', 'Shon McGregory', 'Ilyssa Fradin']
8 Salvation Boulevard ['Jennifer Connelly', 'Marisa Tomei', 'Pierce Brosnan', 'Ed Harris', 'Greg Kinnear', 'Isabelle Fuhrman', 'Howard Hesseman', 'Jim Gaffigan']
6 Saint Ralph ['Adam Butcher', 'Campbell Scott', 'Michael Kanev', 'Gordon Pinsent', 'Tamara Hope', 'Keir Gilchrist']
4 Miss Julie ['Jessica Chastain', 'Colin Farrell', 'Samantha Morton', 'Nora McMenamy']
5 Dum Maaro Dum ['Abhishek Bachchan', 'Bipasha Basu', 'Deepika Padukone', 'Rana Daggubati', 'Prateik Babbar']
9 The Lazarus Effect ['Olivia Wilde', 'Mark Duplass', 'Donald Glover', 'Evan Peters', 'Sarah Bolger', 'Ray Wise', 'Amy Aquino', 'Bruno Gunn', 'Sean T. Krishnan']
9 House Party 2 ['Martin Lawrence', 'Christopher Martin', 'Christopher Reid', 'Paul Anthony', 'Tisha Campbell-Martin', 'Queen Latifah', 'Georg Stanford Brown', 'Whoopi Goldberg', 'Iman']
4 Doug's 1st Movie ['Thomas McHugh', 'Fred Newman', 'Chris Phillips', 'Constance Shulman']
9 The Apostle ['Robert Duvall', 'Billy Bob Thornton', 'June Carter Cash', 'Farrah Fawcett', 'Miranda Richardson', 'Todd Allen', 'Walton Goggins', 'Billy Joe Shaver', 'Renée Victor']
9 Solomon and Sheba ['Yul Brynner', 'Gina Lollobrigida', 'George Sanders', 'Marisa Pavan', 'David Farrar', 'John Crawford', 'Finlay Currie', 'Harry Andrews', 'José Nieto']
7 Not Easily Broken ['Morris Chestnut', 'Taraji P. Henson', 'Maeve Quinlan', 'Kevin Hart', 'Jenifer Lewis', 'Eddie Cibrian', 'Wood Harris']
9 A Farewell to Arms ['Helen Hayes', 'Gary Cooper', 'Adolphe Menjou', 'Mary Philips', 'Jack La Rue', 'Blanche Friderici', 'Mary Forbes', 'Gilbert Emery', 'Agostino Borgato']
9 Digimon: The Movie ['Lara Jill Miller', 'Joshua Seth', 'Bob Papenbrook', 'Doug Berholt', 'Steve Blum', "Colleen O'Shaughnessey", 'Michael Reisz', 'Wendee Lee', 'Brianne Siddall']
8 Robin and Marian ['Sean Connery', 'Audrey Hepburn', 'Robert Shaw', 'Richard Harris', 'Nicol Williamson', 'Ian Holm', 'Ronnie Barker', 'Denholm Elliott']
5 Sea Rex 3D: Journey to a Prehistoric World ['Guillaume Denaiffe', 'Norbert Ferrer', 'Chloe Hollings', 'Richard Rider', 'Tom Yang']
9 The Sweet Hereafter ['Ian Holm', 'Caerthan Banks', 'Sarah Polley', 'Tom McCamus', 'Gabrielle Rose', 'Alberta Watson', 'Maury Chaykin', 'Stephanie Morgenstern', 'Bruce Greenwood']
9 Light Sleeper ['Willem Dafoe', 'Susan Sarandon', 'Dana Delany', 'David Clennon', 'Mary Beth Hurt', 'Victor Garber', 'Jane Adams', 'Sam Rockwell', 'David Spade']
7 The Oh in Ohio ['Parker Posey', 'Danny DeVito', 'Paul Rudd', 'Mischa Barton', 'Miranda Bailey', 'Keith David', 'Heather Graham']
5 Gandhi, My Father ['Darshan Jariwala', 'Akshaye Khanna', 'Bhumika Chawla', 'Shefali Shah', 'Vinay Jain']
5 Out of the Blue ['Dennis Hopper', 'Raymond Burr', 'Sharon Farrell', 'Linda Manz', 'Don Gordon']
5 Out of the Blue ['Dennis Hopper', 'Raymond Burr', 'Sharon Farrell', 'Linda Manz', 'Don Gordon']
4 Lovely, Still ['Martin Landau', 'Ellen Burstyn', 'Adam Scott', 'Elizabeth Banks']
8 Tycoon ['John Wayne', 'Laraine Day', 'Cedric Hardwicke', 'Judith Anderson', 'Anthony Quinn', 'James Gleason', 'Grant Withers', 'Paul Fix']
5 Redacted ['Izzy Diaz', 'Rob Devaney', 'Ty Jones', 'Anas Wellman', 'Mike Figueroa']
9 Fascination ['Jacqueline Bisset', 'Adam Garcia', 'James Naughton', 'Stuart Wilson', 'Alice Evans', 'Cachaco', 'Elia Enid Cadilla', 'Idée Charriez', 'Jaime Bello']
9 Born Of War ['James Frain', "Sofia Black-D'Elia", 'Lydia Leonard', 'Joey Ansah', 'Michael Maloney', 'Michael Brandon', 'Jade Hudson', 'Avin Shah', 'Lisa Kay']
0 Running Forever []
9 I Served the King of England ['Ivan Barnev', 'Oldřich Kaiser', 'Julia Jentsch', 'Marián Labuda', 'Martin Huba', 'Milan Lasica', 'Josef Abrhám', 'Jaromír Dulava', 'Jiří Lábus']
8 Let's Kill Ward's Wife ['Patrick Wilson', 'Scott Foley', 'Amy Acker', 'Donald Faison', 'Dagmara Domińczyk', 'Nicollette Sheridan', 'Greg Grunberg', 'Marika Dominczyk']
9 Camping Sauvage ['Denis Lavant', 'Isild Le Besco', 'Pascal Bongard', 'Jean-Michel Guerin', 'Martine Demaret', 'Raphaëlle Misrahi', 'Emmanuelle Bercot', 'Marcel Fix', 'Yann Trégouët']
6 All Hat ['Rachael Leigh Cook', 'Luke Kirby', 'Keith Carradine', 'Lisa Ray', 'Graham Greene', 'Ernie Hudson']
7 Treading Water ['Douglas Smith', 'Zoë Kravitz', 'Ariadna Gil', 'Don McKellar', 'Kim Ly', 'Gonzalo Vega', 'Carrie-Anne Moss']
4 Tango ['Miguel Ángel Solá', 'Cecilia Narova', 'Mía Maestro', 'Juan Carlos Copes']
5 Saving Private Perez ['Joaquín Cosio', 'Gerardo Taracena', 'Jaime Camil', 'Miguel Rodarte', 'Jesús Ochoa']
4 Character ['Jan Decleir', 'Fedja van Huêt', 'Betty Schuurman', 'Tamar van den Dop']
4 Mozart's Sister ['Marie Féret', 'Marc Barbé', 'Delphine Chuillot', 'David Moreau']
5 Lilya 4-ever ['Oksana Akinshina', 'Artyom Bogucharsky', 'Lyubov Agapova', 'Liliya Shinkaryova', 'Elina Benenson']
6 Fugly ['Jimmy Shergill', 'Mohit Marwah', 'Kiara Advani', 'Vijendar Singh', 'Arfi Lamba', 'Anshuman Jha']
8 Anne of Green Gables ['Megan Follows', 'Colleen Dewhurst', 'Richard Farnsworth', 'Patricia Hamilton', 'Marilyn Lightstone', 'Schuyler Grant', 'Jonathan Crombie', 'Charmion King']
8 Sexy Beast ['Ray Winstone', 'Ben Kingsley', 'Ian McShane', 'Amanda Redman', 'James Fox', 'Cavan Kendall', 'Julianne White', 'Álvaro Monje']
7 Paa ['Amitabh Bachchan', 'Abhishek Bachchan', 'Vidya Balan', 'Paresh Rawal', 'Arundathi Nag', 'Swini Khera', 'Jaya Bachchan']
8 Love and Death on Long Island ['John Hurt', 'Jason Priestley', 'Sheila Hancock', 'Maury Chaykin', 'Fiona Loewi', 'Harvey Atkin', 'Gawn Grainger', 'Elizabeth Quinn']
8 Survival of the Dead ['Alan van Sprang', 'Kenneth Welsh', 'Kathleen Munroe', 'Devon Bostick', 'Richard Fitzpatrick', 'Athena Karkanis', 'Stefano DiMatteo', 'Julian Richings']
7 Hansel and Gretel Get Baked ['Molly C. Quinn', 'Michael Welch', 'Lara Flynn Boyle', 'Cary Elwes', 'Lochlyn Munro', 'Yancy Butler', 'Bianca Saad']
5 What the #$*! Do We (K)now!? ['Marlee Matlin', 'Elaine Hendrix', 'Robert Blanche', 'John Ross Bowie', 'Robert Bailey Jr.']
7 The Last Exorcism Part II ['Ashley Bell', 'Julia Garner', 'Andrew Sensenig', 'Spencer Treat Clark', 'Judd Lormand', 'Muse Watson', 'Raeden Greer']
9 The Wash ['Dr. Dre', 'Snoop Dogg', 'DJ Pooh', 'Angell Conwell', 'Bruce Bruce', 'Eminem', 'Tom Lister Jr.', 'Alex Thomas', 'Shari Watson']
9 The Jerky Boys ['John G. Brennan', 'Kamal Ahmed', 'Alan Arkin', 'William Hickey', 'Vincent Pastore', 'Alan North', 'Suzanne Shepherd', 'Peter Appel', 'Ozzy Osbourne']
9 Secretary ['James Spader', 'Maggie Gyllenhaal', 'Jeremy Davies', 'Lesley Ann Warren', 'Stephen McHattie', 'Amy Locane', 'Patrick Bauchau', 'Jessica Tuck', 'Oz Perkins']
1 The Real Cancun ['Laura Ramsey']
7 Talk Radio ['Eric Bogosian', 'Ellen Greene', 'Leslie Hope', 'John C. McGinley', 'Alec Baldwin', 'John Pankow', 'Anna Levine']
8 Love Stinks ['French Stewart', 'Bridgette Wilson', 'Bill Bellamy', 'Tyra Banks', 'Tiffani Thiessen', 'Colleen Camp', "John O'Hurley", 'Ivana Miličević']
8 Thumbsucker ['Lou Taylor Pucci', 'Tilda Swinton', "Vincent D'Onofrio", 'Keanu Reeves', 'Benjamin Bratt', 'Vince Vaughn', 'Kelli Garner', 'Chase Offerle']
4 Samsara ['Marcos Luna', 'Putu Dinda Pratika', 'Puti Sri Candra Dewi', 'Ni Made Megahadi Pratiwi']
7 Poolhall Junkies ['Ricky Schroder', 'Chazz Palminteri', 'Rod Steiger', 'Michael Rosenbaum', 'Mars Callahan', 'Alison Eastwood', 'Christopher Walken']
8 An Everlasting Piece ['Barry McEvoy', "Brían F. O'Byrne", 'Anna Friel', 'Pauline McLynn', 'Ruth McCabe', 'Billy Connolly', 'Des McAleer', 'Laurence Kinlan']
7 Among Giants ['Pete Postlethwaite', 'Rachel Griffiths', 'Andy Serkis', 'Lennie James', 'James Thornton', 'Rob Jarvis', 'Alan Williams']
4 The Velocity of Gary ["Vincent D'Onofrio", 'Salma Hayek', 'Thomas Jane', "Olivia d'Abo"]
6 Futuro Beach ['Wagner Moura', 'Clemens Schick', 'Jesuíta Barbosa', 'Sabine Timoteo', 'Sophie Charlotte Conrad', 'Demick Lopes']
4 Nothing ['David Hewlett', 'Andrew Miller', 'Gordon Pinsent', 'Marie-Josée Croze']
7 The Geographer Drank His Globe Away ['Konstantin Khabenskiy', 'Elena Lyadova', 'Aleksandr Robak', 'Evgeniya Khirivskaya', 'Agrippina Steklova', 'Andrey Prytkov', 'Anfisa Chernykh']
7 Inescapable ['Alexander Siddig', 'Joshua Jackson', 'Marisa Tomei', 'Oded Fehr', 'Saad Siddiqui', 'Fadia Nadda', 'Bonnie Lee Bouman']
9 Hell's Angels ['Ben Lyon', 'James Hall', 'Jean Harlow', 'John Darrow', 'Lucien Prival', 'Frank Clarke', 'Roy Wilson', 'Douglas Gilmore', 'Jane Winton']
9 The Loved Ones ['Xavier Samuel', 'Jessica McNamee', 'Robin McLeavy', 'Victoria Thaine', 'John Brumpton', 'Fred Whitlock', 'Eden Porter', 'Richard Wilson', 'Stephen Walden']
6 The Perfect Wave ['Scott Eastwood', 'Cheryl Ladd', 'Patrick Lyster', 'Rachel Hendrix ', 'Scott Mortensen', 'Nikolai Mynhardt']
6 Annie Get Your Gun ['Betty Hutton', 'Howard Keel', 'Louis Calhern', 'J. Carrol Naish', 'Edward Arnold', 'Keenan Wynn']
4 Chain of Command ['Michael Jai White', 'Steve Austin', 'Max Ryan', 'Allen Yates']
4 I Got the Hook Up ['Master P', 'Anthony Johnson', 'Ice Cube', 'Tom Lister Jr.']
8 She's the One ['Edward Burns', 'Michael McGlone', 'Cameron Diaz', 'Jennifer Aniston', 'John Mahoney', 'Maxine Bahns', 'Leslie Mann', 'Amanda Peet']
5 Train ['Thora Birch', 'Gideon Emery', 'Gloria Votsis', 'Derek Magyar', 'Todd Jensen']
9 Evil Dead II ['Bruce Campbell', 'Sarah Berry', 'Dan Hicks', 'Kassie DePaiva', 'Denise Bixler', 'Richard Domeier', 'John Peakes', 'Lou Hancock', 'Ted Raimi']
5 The Other Conquest ['Damián Delgado', 'José Carlos Rodríguez', 'Elpidia Carrillo', 'Iñaki Aierra', 'Honorato Magaloni']
7 Troll Hunter ['Otto Jespersen', 'Hans Morten Hansen', 'Tomas Alf Larsen', 'Johanna Mørck', 'Knut Nærum', 'Robert Stoltenberg', 'Glenn Erland Tosterud']
6 The Masked Saint ['Brett Granstaff', 'Lara Jean Chorostecki', 'T.J. McGibbon', 'Diahann Carroll', 'Roddy Piper', 'James Preston Rogers']
9 The Betrayed ['Melissa George', 'Oded Fehr', 'Christian Campbell', 'Alice Krige', 'Connor Christopher Levins', 'Donald Adams', 'Phillip Mitchell', 'Kevan Kase', 'Scott Heindl']
6 Taxman ['Joe Pantoliano', 'Wade Dominguez', 'Elizabeth Berkley', 'Michael Chiklis', 'Robert Townsend', 'Fisher Stevens']
9 The Secret ['James Nesbitt', "Genevieve O'Reilly", 'Jason Watkins', 'Laura Pyper', 'Glen Wallace', 'Stuart Graham', 'Liam McMahon', 'James Greene', 'B.J. Hogg']
4 2:13 ['Mark Thompson', 'Mark Pellegrino', 'Teri Polo', 'Kevin Pollak']
5 Time to Choose ['Oscar Isaac', 'Jane Goodall', 'Jerry Brown', 'Neal Barnard', 'Michael Pollan']
5 In the Name of the King III ['Dominic Purcell', 'Ralitsa Paskaleva', 'Bashar Rahal', 'Nikolai Sotirov', 'Marian Valev']
5 Stranded ['Scott Eastwood', 'Rita Wilson', 'Jeff Fahey', 'David James Elliott', 'Kim Matula']
6 Lords of London ['Glen Murphy', 'Ray Winstone', 'Giovanni Capalbo', 'Serena Iansiti', 'Christopher Hatherhall', 'Joe Egan']
4 March of the Penguins ['Morgan Freeman', 'Charles Berling', 'Romane Bohringer', 'Jules Sitruk']
3 August ['Murray Bartlett', 'Daniel Dugan', 'Adrian Gonzalez']
9 Human Traffic ['John Simm', 'Danny Dyer', 'Lorraine Pilkington', 'Shaun Parkes', 'Nicola Reynolds', 'Terence Beesley', 'Jo Brand', 'Richard Coyle', 'Andrew Lincoln']
7 The Opposite Sex ['Mena Suvari', 'Eric Roberts', 'Kristin Chenoweth', 'Dana Ashbrook', 'Kenan Thompson', 'Jennifer Finnigan', 'Danielle Guldin']
7 Dreaming of Joseph Lees ['Rupert Graves', 'Samantha Morton', 'Nicholas Woodeson', 'Lee Ross', 'Felix Billson', 'Lauren Richardson', 'Vernon Dobtcheff']
4 The Original Kings of Comedy ['Steve Harvey', 'D. L. Hughley', 'Cedric the Entertainer', 'Bernie Mac']
1 Martin Lawrence Live: Runteldat ['Martin Lawrence']
8 Air Bud ['Kevin Zegers', 'Wendy Makkena', 'Michael Jeter', 'Bill Cobbs', 'Brendan Fletcher', 'Norman Browning', 'Eric Christmas', 'Nicola Cavendish']
3 Pokémon: Spell of the Unknown ['Veronica Taylor', 'Rachael Lillis', 'Eric Stuart']
4 Spaced Invaders ['Ariana Richards', 'Douglas Barr', 'Royal Dano', 'William Holmes']
9 Slow West ['Michael Fassbender', 'Kodi Smit-McPhee', 'Ben Mendelsohn', 'Caren Pistorius', 'Rory McCann', 'Brooke Williams', 'Alex MacQueen', 'Kalani Queypo', 'Madeleine Sami']
6 Next Day Air ['Donald Faison', 'Mike Epps', 'Wood Harris', 'Omari Hardwick', 'Yasiin Bey', 'Lauren London']
5 Trippin' ['Deon Richmond', 'Donald Faison', 'Guy Torry', 'Maia Campbell', 'Aloma Wright']
5 Phat Girlz ["Mo'Nique", 'Jimmy Jean-Louis', 'Godfrey', 'Joyful Drake', 'Brendan Walsh']
5 Woman Thou Art Loosed ['Kimberly Elise', 'Loretta Devine', 'Debbi Morgan', 'Michael Boatman', 'Louisa Abernathy']
7 Real Women Have Curves ['America Ferrera', 'Lupe Ontiveros', 'Ingrid Oliu', 'George Lopez', 'Brian Sites', 'Soledad St. Hilaire', 'Marlene Forte']
9 Water ['Lisa Ray', 'Sarala', 'John Abraham', 'Seema Biswas', 'Waheeda Rehman', 'Vinay Pathak', 'Rishma Malik', 'Manorama', 'Raghuvir Yadav']
9 Whipped ['Amanda Peet', 'Brian Van Holt', 'Jonathan Abrahams', 'Zorie Barber', 'Judah Domke', 'Callie Thorne', 'Bridget Moynahan', 'Taryn Reif', 'Neriah Davis']
4 Kama Sutra - A Tale of Love ['Indira Varma', 'Sarita Choudhury', 'Ramon Tikaram', 'Naveen Andrews']
7 Days of Heaven ['Richard Gere', 'Brooke Adams', 'Linda Manz', 'Sam Shepard', 'Robert J. Wilke', 'Stuart Margolin', 'Timothy Scott']
4 DysFunktional Family ['Eddie Griffin', 'Joe Howard', 'Matthew Brent', 'Robert Noble']
5 Hobo with a Shotgun ['Rutger Hauer', 'Gregory Smith', 'Robb Wells', 'Brian Downey', 'Molly Dunsworth']
9 Compadres ['Omar Chaparro', 'Joey Morgan', 'Aislinn Derbez', 'Eric Roberts', 'Camila Sodi', 'Kevin Pollak', 'Armando Hernández', 'Erick Elías', 'José Sefami']
5 Love's Abiding Joy ['Erin Cottrell', 'Logan Bartholomew', 'William Morgan Sheppard', 'James Tupper', 'Irene Bedard']
7 Brave New Girl ['Virginia Madsen', 'Lindsey Haun', 'Barbara Mamabolo', 'John Ralston', 'Nick Roth', 'Joanne Boland', 'Aaron Ashmore']
6 Fort McCoy ['Eric Stoltz', 'Kate Connor', 'Lyndsy Fonseca', 'Andy Hirsch', 'Camryn Manheim', 'Seymour Cassel']
8 Chain Letter ['Nikki Reed', 'Keith David', 'Brad Dourif', 'Betsy Russell', 'Cherilyn Wilson', 'Noah Segan', 'Matt Cohen', 'Bai Ling']
7 Just Looking ['Gretchen Mol', 'Patti LuPone', 'Peter Onorati', 'Ryan Merriman', 'Richard V. Licata', 'Marcell Rosenblatt', "Deirdre O'Connell"]
5 The Eclipse ['Ciarán Hinds', 'Aidan Quinn', 'Iben Hjejle', 'Jim Norton', 'Valerie Spelman']
6 Four Single Fathers ['Alessandro Gassman', 'Francesco Quinn', 'Joe Urla', 'Lenny Venito', 'Jennifer Esposito', 'J. Jewels']
6 Enter the Dangerous Mind ['Jake Hoffman', 'Nikki Reed', 'Thomas Dekker', 'Scott Bakula', 'Jason Priestley', 'Gina Rodriguez']
4 Iguana ['Everett McGill', 'Fabio Testi', 'Michael Madsen', 'Jack Taylor']
6 Chicago Overcoat ['Frank Vincent', 'Kathrine Narducci', 'Mike Starr', 'Stacy Keach', 'Armand Assante', 'Danny Goldring']
6 Close Range ['Scott Adkins', 'Nick Chinlund', 'Caitlin Keats', 'Jake La Botz', 'Tony Perez', 'Madison Lawlor']
3 Boynton Beach Club ['Brenda Vaccaro', 'Dyan Cannon', 'Joseph Bologna']
6 Amnesiac ['Kate Bosworth', 'Wes Bentley', 'Shashawnee Hall', 'Richard Riehle', 'Patrick Bauchau', 'Olivia Rose Keegan']
7 High Tension ['Cécile de France', 'Maïwenn', 'Philippe Nahon', 'Franck Khalfoun', 'Andrei Finti', 'Oana Pellea', 'Marco Claudiu Pascu']
6 Griff the Invisible ['Ryan Kwanten', 'Maeve Dermody', 'Marshall Napier', 'Heather Mitchell', 'Patrick Brammall', 'Kelly Paterniti']
9 The Black Stallion ['Kelly Reno', 'Mickey Rooney', 'Teri Garr', 'Clarence Muse', 'Hoyt Axton', 'Michael Higgins', 'Ed McNamara', 'Doghmi Larbi', 'Cass-Olé']
0 Sardaarji []
6 Journey to Saturn ['Casper Christensen', 'Frank Hvam', 'Ali Kazim', 'Iben Hjejle', 'Peter Belli', 'Lars Hjortshøj']
8 Timecrimes ['Karra Elejalde', 'Candela Fernández', 'Bárbara Goenaga', 'Nacho Vigalondo', 'Juan Inciarte', 'Libby Brien', 'Nicole Dionne', 'Philip Hersh']
7 Silver Medalist ['Huang Bo', 'Kong Jiu', 'Shaohua Ma', 'Xu Zheng', 'Yung Cheung', 'Shuangbao Wang', 'Liu Gang']
5 Fat, Sick & Nearly Dead ['Joe Cross', 'Phil Riverstone', 'Amy Badberg', 'Merv Cross', 'Virginia Cross']
0 2016: Obama's America []
7 Kevin Hart: Let Me Explain ['Kevin Hart', 'David Terrell', 'David Jason Perez', 'Justine Herron', 'Harry Ratchford', 'Joey Wells', 'William Horton']
9 Jesus' Son ['Billy Crudup', 'Denis Leary', 'Jack Black', 'Dennis Hopper', 'Holly Hunter', 'Samantha Morton', 'Miranda July', 'Michael Shannon', 'Mark Webber']
5 Saving Face ['Michelle Krusiec', 'Joan Chen', 'Lynn Chen', 'Ato Essandoh', 'Jessica Hecht']
5 Brick Lane ['Tannishtha Chatterjee', 'Satish Kaushik', 'Christopher Simpson', 'Naeema Begum', 'Lana Rahman']
6 Fuel ['Joshua Tickell', 'Barbara Boxer', 'Richard Branson', 'George W. Bush', 'Sheryl Crow', 'Larry David']
4 Valley of the Heart's Delight ['Pete Postlethwaite', 'Gabriel Mann', 'Emily Harrison', 'Diana Scarwid']
6 8: The Mormon Proposition ['Rocky Mayor Anderson', 'Matt Aune', 'Tyler Barrick', 'Bruce Barton', 'Melissa Bird', 'Dustin Lance Black']
3 Sleep Dealer ['Leonor Varela', 'Jacob Vargas', 'Luis Fernando Peña']
8 Christmas Mail ['Ashley Scott', 'A.J. Buckley', 'Rolanda Watts', 'Vanessa Evigan', 'Lochlyn Munro', 'Piper Mackenzie Harris', 'Paris Tanaka', 'Ron Roggé']
6 Thr3e ['Marc Blucas', 'Justine Waddell', 'Bill Moseley', 'Priscilla Barnes', 'Jack Ryan', 'Kevin Downes']
4 Go for It! ['Aimee Garcia', 'Al Bandiero', 'Jossara Jinaro', 'Gina Rodriguez']
7 Redemption Road ['Michael Clarke Duncan', 'Morgan Simpson', 'Kiele Sanchez', 'Taryn Manning', 'Luke Perry', 'Tom Skerritt', 'Lee Perkins']
4 Fantasia ['Deems Taylor', 'Walt Disney', 'Julietta Novis', 'Leopold Stokowski']
4 8 Days ['Nicole Smolen', 'Kim Baldwin', 'Ariana Stephens', 'Bryson Funk']
7 Impact Point ['Brian Austin Green', 'Melissa Keller', 'Linden Ashby', 'Joe Manganiello', 'Eddie Alfano', 'Ron Roggé', 'Kayla Ewell']
7 Elling ['Per Christian Ellefsen', 'Sven Nordin', 'Jørgen Langhelle', 'Marit Pia Jacobsen', 'Per Christensen', 'Hilde Olausson', 'Ola Otnes']
5 Mi America ['Robert Fontaine', 'Michael Brainard', 'Grant Boyd', 'Michael Derek', 'Lily Autumn Page']
5 Lies in Plain Sight ['Martha Higareda', 'Chad Michael Murray', 'Yul Vazquez', 'Benito Martinez', 'Cheyenne Haynes']
0 Sharkskin []
8 Containment ['Louise Brealey', 'Lee Ross', 'Sheila Reid', 'Pippa Nixon', 'Claire Greasley', 'Andrew Leung', 'Billy Postlethwaite', 'Hannah Chalmers']
8 The Timber ['James Ransone', 'Elisa Lasowski', 'Josh Peck', 'Attila Árpa', 'William Gaunt', 'David Bailie', "Shaun O'Hagan", 'Maria Doyle Kennedy']
9 Sleeper ['Woody Allen', 'Diane Keaton', 'John Beck', 'Mary Gregory', 'Brian Avery', 'Don Keefer', 'Mews Small', 'Peter Hobbs', 'Spencer Milligan']
6 Silent House ['Elizabeth Olsen', 'Adam Trese', 'Eric Sheffer Stevens', 'Julia Taylor Ross', 'Adam Barnett', 'Haley Murphy']
7 The Triplets of Belleville ['Béatrice Bonifassi', 'Lina Boudreau', 'Michèle Caucheteux', 'Jean-Claude Donda', 'Mari-Lou Gauthier', 'Charles Linton', 'Suzy Falk']
6 Touching the Void ['Brendan Mackey', 'Nicholas Aaron', 'Richard Hawking', 'Ollie Ryall', 'Joe Simpson', 'Simon Yates']
9 Inside Job ['Matt Damon', 'William Ackman', 'Barack Obama', 'George W. Bush', 'Jonathan Alpert', 'Christine Lagarde', 'Ann Curry', 'Daniel Alpert', 'Sigridur Benediktsdottir']
4 Waltz with Bashir ['Ari Folman', 'Ron Ben-Yishai', 'Dror Harazi', 'Ronny Dayag']
2 The Book of Mormon Movie, Volume 1: The Journey ['Kirby Heyborne', 'Michael Flynn']
4 No End in Sight ['Campbell Scott', 'Gerald Burke', 'Ali Fadhil', 'Robert Hutchings']
9 In the Shadow of the Moon ['Buzz Aldrin', 'Michael Collins', 'Alan Bean', 'Eugene Cernan', 'Charles Duke', 'James Lovell', 'Edgar Mitchell', 'Harrison Schmitt', 'John Young']
9 Meek's Cutoff ['Michelle Williams', 'Bruce Greenwood', 'Will Patton', 'Zoe Kazan', 'Paul Dano', 'Shirley Henderson', 'Neal Huff', 'Tommy Nelson', 'Rod Rondeaux']
4 Inside Deep Throat ['Dennis Hopper', 'Peter Bart', 'Warren Beatty', 'Carl Bernstein']
8 The Virginity Hit ['Matt Bennett', 'Zack Pearlman', 'Jacob Davich', 'Justin Kline', 'Krysta Rodriguez', 'Nicole Weaver', 'Savannah Welch', 'Tina Parker']
8 Subway ['Isabelle Adjani', 'Christopher Lambert', 'Richard Bohringer', 'Michel Galabru', 'Jean-Hugues Anglade', 'Jean Reno', 'Jean-Pierre Bacri', 'Jean Bouise']
7 Teeth ['Jess Weixler', 'John Hensley', 'Josh Pais', 'Hale Appleman', 'Lenny Von Dohlen', 'Vivienne Benesch', 'Ashley Springer']
0 Hum To Mohabbat Karega []
6 Saint John of Las Vegas ['Steve Buscemi', 'Romany Malco', 'Tim Blake Nelson', 'Sarah Silverman', 'John Cho', 'Emmanuelle Chriqui']
5 Roadside Romeo ['Saif Ali Khan', 'Kareena Kapoor', 'Javed Jaffrey', 'Tanaaz Currim Irani', 'Vrajesh Hirjee']
8 This Thing of Ours ['James Caan', 'James Caan', 'Frank Vincent', 'Vincent Pastore', 'Louis Vanaria', 'Christian Maelen', 'Edward Lynch', 'Chuck Zito']
9 The Lost Medallion: The Adventures of Billy Stone ['William Brent', 'Sammi Hanratty', 'James Hong', 'Alex Kendrick', 'Mark Dacascos', 'Jansen Panettiere', 'Tiya Sircar', 'William Corkery', 'Marlowe Peyton']
8 Sherrybaby ['Maggie Gyllenhaal', 'Michelle Hurst', 'Sandra Rodríguez', 'Danny Trejo', 'Brad William Henke', 'Sam Bottoms', 'Giancarlo Esposito', 'Bridget Barkan']
4 Freeze Frame ['Lee Evans', 'Sean McGinley', 'Ian McNeice', 'Colin Salmon']
4 Stitches ['Ross Noble', 'Tommy Knight', 'Gemma-Leah Devereux', 'John McDonnell']
9 Nine Dead ['Melissa Joan Hart', 'John Terry', 'Chip Bent', 'Lawrence Turner', 'Edrick Browne', 'John Cates', 'Marc Macaulay', 'Lucille Soong', 'Ritchie Montgomery']
1 To Be Frank, Sinatra at 100 ['Tony Oppedisano']
8 No Man's Land: The Rise of Reeker ['Stephen Martines', 'Valerie Cruz', 'Mircea Monroe', 'Desmond Askew', 'Michael Robert Brandon', 'Michael Muhney', 'David Stanbra', 'Robert Pine']
8 Highway ['Jake Gyllenhaal', 'Selma Blair', 'Jared Leto', 'John C. McGinley', 'Jeremy Piven', 'Kimberley Kates', 'Mark Rolston', 'Arden Myrin']
7 The Ghastly Love of Johnny X ['Will Keenan', 'Creed Bratton', 'De Anna Joy Brooks', 'Reggie Bannister', 'Jed Rowen', 'Kate Maberly', 'Paul Williams']
7 The Torture Chamber of Dr. Sadism ['Lex Barker', 'Christopher Lee', 'Karin Dor', 'Carl Lange', 'Christiane Rücker', 'Vladimir Medar', 'Dieter Eppler']
7 River's Edge ['Crispin Glover', 'Keanu Reeves', 'Ione Skye', 'Daniel Roebuck', 'Dennis Hopper', 'Taylor Negron', 'Joshua John Miller']
7 The Square ['Khalid Abdalla', 'Dina Abdullah', 'Dina Amer', 'Magdy Ashour', 'Ramy Essam', 'Ahmed Hassan', 'Aida Elkashef']
8 Man on Wire ['Philippe Petit', 'Jean François Heckel', 'Jean-Louis Blondeau', 'Annie Allix', 'David Forman', 'Alan Welner', 'Barry Greenhouse', 'Jim Moore']
5 Brotherly Love ['Keke Palmer', 'Cory Hardrict', 'Eric D. Hill Jr.', 'Quincy Brown', 'Nafessa Williams']
8 The Last Exorcism ['Ashley Bell', 'Patrick Fabian', 'Iris Bahr', 'Louis Herthum', 'Caleb Landry Jones', 'Shanna Forrestall', 'Tony Bentley', 'Allen Boudreaux']
7 The Greatest Movie Ever Sold ['Morgan Spurlock', 'Peter Berg', 'Paul Brennan', 'Ralph Nader', 'Brett Ratner', 'J.J. Abrams', 'Donald Trump']
6 Ed and His Dead Mother ['Eric Christmas', 'Harper Roisman', 'Steve Buscemi', 'Sam Jenkins', 'Ned Beatty', 'Miriam Margolyes']
5 Travellers and Magicians ['Tshewang Dendup', 'Sonam Lhamo', 'Lhakpa Dorji', 'Deki Yangzom', 'Sonam Kinga']
5 A Beginner's Guide to Snuff ['Joey Kern', 'Luke Edwards', 'Bree Williamson', 'Brad Greenquist', 'Perry Laylon Ojeda']
5 Independence Daysaster ['Casey Dubois', 'Iain Belcher', 'Andrea Brooks', 'Nicholas Carella', 'Emily Holmes']
9 Against the Wild ['Natasha Henstridge', 'CJ Adams', 'Erin Pitt', 'Ted Whittall', 'Rainbow Francks', 'John Tench', 'Jennifer Gibson', 'Houston', 'Barney']
9 I Spit on Your Grave ['Sarah Butler', 'Daniel Franzese', 'Chad Lindberg', 'Jeff Branson', 'Rodney Eastman', 'Andrew Howard', 'Tracey Walter', 'Mollie Milligan', 'Saxon Sharbino']
9 Happy, Texas ['Steve Zahn', 'William H. Macy', 'Jeremy Northam', 'Ally Walker', 'Ron Perlman', 'Illeana Douglas', 'M.C. Gainey', 'Mo Gaffney', 'Paul Dooley']
4 My Summer of Love ['Natalie Press', 'Emily Blunt', 'Paddy Considine', 'Dean Andrews']
9 The Lunchbox ['Irrfan Khan', 'Nimrat Kaur', 'Nawazuddin Siddiqui', 'Denzil Smith', 'Bharati Achrekar', 'Nakul Vaid', 'Yashvi Puneet Nagar', 'Lillete Dubey', 'Shruti Bapna']
7 Yes ['Joan Allen', 'Simon Abkarian', 'Sam Neill', 'Shirley Henderson', 'Stephanie Leonidas', 'Sheila Hancock', 'Gary Lewis']
8 Grace Unplugged ['AJ Michalka', 'James Denton', 'Kevin Pollak', 'Shawnee Smith', 'Michael Welch', 'Jamie Grace', 'Emma Catherwood', 'Zane Holtz']
6 N-Secure ['Cordell Moore', 'Essence Atkins', 'Denise Boutte', 'Tempestt Bledsoe', 'Lamman Rucker', 'Toni Trucks']
6 Out of the Dark ['Julia Stiles', 'Scott Speedman', 'Stephen Rea', 'Alejandro Furth', 'Pixie Davies', 'Guillermo Morales Vitola']
8 The Bubble ['Ohad Knoller', 'Yousef Sweid', 'Daniella Wircer', 'Alon Friedman', 'Zion Baruch', 'Ruba Blal', 'Oded Leopold', 'Zohar Liba']
8 Mississippi Mermaid ['Jean-Paul Belmondo', 'Catherine Deneuve', 'Michel Bouquet', 'Nelly Borgeaud', 'Martine Ferrière', 'Marcel Berbert', 'Yves Drouhet', 'Roland Thénot']
9 Bloodsport ['Jean-Claude Van Damme', 'Bolo Yeung', 'Roy Chiao', 'Philip Chan Yan-Kin', 'Donald Gibb', 'Ken Siu', 'Leah Ayres', 'Normann Burton', 'Forest Whitaker']
9 Kissing Jessica Stein ['Jennifer Westfeldt', 'Tovah Feldshuh', 'Esther Wurmfeld', 'Hillel Friedman', 'Jon Hamm', 'Scott Cohen', 'Ben Weber', 'Brian Stepanek', 'Jennifer Carta']
8 Kickboxer: Vengeance ['Alain Moussi', 'Dave Bautista', 'Sara Malakul Lane', 'Jean-Claude Van Damme', 'Darren Shahlavi', 'Georges St-Pierre', 'Gina Carano', 'Gino Galento']
6 The Gatekeepers ['Ami Ayalon', 'Avraham Shalom', 'Yaakov Peri', 'Carmi Gillon', 'Avi Dichter', 'Yuval Diskin']
9 The Ballad of Jack and Rose ['Daniel Day-Lewis', 'Camilla Belle', 'Catherine Keener', 'Ryan McDonald', 'Paul Dano', 'Jason Lee', 'Jena Malone', 'Beau Bridges', 'Susanna Thompson']
4 Unsullied ['Rusty Joiner', 'Murray Gray', 'James Gaudioso', 'Erin Boyes']
9 Session 9 ['Peter Mullan', 'David Caruso', 'Stephen Gevedon', 'Josh Lucas', 'Brendan Sexton III', 'Paul Guilfoyle', 'Larry Fessenden', 'Charley Broderick', 'Lonnie Farmer']
5 I Want Someone to Eat Cheese With ['Jeff Garlin', 'Sarah Silverman', 'Bonnie Hunt', 'Elle Fanning', 'Jessy Schram']
4 Mooz-lum ['Nia Long', 'Danny Glover', 'Evan Ross', 'Summer Bishil']
7 My Name Is Bruce ['Bruce Campbell', 'Grace Thorsen', 'Ted Raimi', 'Adam Boyd', 'Mike Estes', 'Janelle Farber', 'Dani Kelly']
7 The Salon ['Dondre Whitfield', 'Kym Whitley', 'Monica Calhoun', 'Terrence Howard', 'Darrin Henson', 'Kelvin Davis', 'Vivica A. Fox']
7 Forty Shades of Blue ['Dina Korzun', 'Rip Torn', 'Darren E. Burrows', 'Andrew Henderson', 'Elizabeth Morton', 'Joanne Pankow', "Jenny O'Hara"]
8 Amigo ['Chris Cooper', 'DJ Qualls', 'Garret Dillahunt', 'Yul Vazquez', 'Lucas Neff', 'Dane DeHaan', 'Joel Torre', 'Bill Tangradi']
0 Me You and Five Bucks []
4 Last I Heard ['Paul Sorvino', 'Chazz Palminteri', 'Michael Rapaport', 'Renee Props']
9 Closer to the Moon ['Vera Farmiga', 'Mark Strong', 'Harry Lloyd', 'Anton Lesser', 'Joe Armstrong', 'Christian McKay', 'Tim Plester', 'Monica Bârlădeanu', 'Allan Corduner']
9 #Horror ['Taryn Manning', 'Natasha Lyonne', 'Chloë Sevigny', 'Balthazar Getty', 'Timothy Hutton', 'Lydia Hearst', 'Jessica Blank', 'Annabelle Dexter-Jones', 'Tara Subkoff']
6 Wind Walkers ['Zane Holtz', 'Glen Powell', 'Kiowa Gordon', 'Castille Landon', 'Johnny Sequoyah', 'Heather Rae']
5 The Holy Girl ['María Alché', 'Mercedes Morán', 'Carlos Belloso', 'Alejandro Urdapilleta', 'Mía Maestro']
4 The Blue Room ['Mathieu Amalric', 'Léa Drucker', 'Stéphanie Cléau', 'Laurent Poitrenaux']
3 The Ballad of Gregorio Cortez ['Edward James Olmos', 'James Gammon', 'Tom Bower']
8 Journey from the Fall ['Kiều Chinh', 'Long Nguyen', 'Diem Lien', 'Jayvee Mai The Hiep', 'Khanh Doan', 'Cat Ly', 'Nguyen Thai Nguyen', 'Tere Morris']
8 The Basket ['Peter Coyote', 'Karen Allen', 'Robert Burke', 'Amber Willenborg', 'Jack MacDonald', 'Eric Dane', 'Brian Skala', 'Patrick Treadway']
5 Queen of the Mountains ['Elina Abai Kyzy', 'Aziz Muradillayev', 'Nasira Mambetov', 'Adilet Usubaliyev', 'Mirlan Abdulayev']
4 The Hebrew Hammer ['Adam Goldberg', 'Judy Greer', 'Andy Dick', 'Mario Van Peebles']
4 The Lion of Judah ['Georgina Cordova', 'Ernest Borgnine', 'Michael Madsen', 'Scott Eastwood']
9 Da Sweet Blood of Jesus ['Felicia Pearson', 'Zaraah Abrahams', 'Elvis Nolasco', 'Steven Hauck', 'Stephen Tyrone Williams', 'Lauren Macklin', 'Rami Malek', 'Thomas Jefferson Byrd', 'Stephen Henderson']
9 Sex, Lies, and Videotape ['Andie MacDowell', 'Peter Gallagher', 'James Spader', 'Laura San Giacomo', 'Ron Vawter', 'Steven Brill', 'Alexandra Root', 'Earl T. Taylor', 'David Foil']
6 The Algerian ['Ben Youcef', 'Candice Coke', 'Harry Lennix', 'Tara Holt', 'Josh Pence', 'Alicia Mitchell']
0 Down & Out With The Dolls []
5 Pink Ribbons, Inc. ['Samantha King', 'Barbara Brenner', 'Barbara Ehrenreich', 'Nancy Brinker', 'Susan Love']
4 Certifiably Jonathan ['Jonathan Winters', 'Robin Williams', 'Sarah Silverman', 'Patricia Arquette']
9 The Blade of Don Juan ['Juan Carlos Montoya', 'Rodrigo Viaggio', 'Irma Maury', 'Antonio Arrué', 'Viviana Andrade', 'Jorge Gutiérrez', 'Nataniel Sánchez', 'Deyssi Pelaez', 'Claudia Solís']
6 Grand Theft Parsons ['Johnny Knoxville', 'Christina Applegate', 'Gabriel Macht', 'Marley Shelton', 'Robert Forster', 'Michael Shannon']
5 Below Zero ['Edward Furlong', 'Michael Berryman', 'Kristin Booth', 'Michael Eisner', 'Dee Hanna']
0 Crowsnest []
8 The Wicked Within ['Sienna Guillory', 'Gianni Capaldi', 'Enzo Cilenti', 'Michele Hicks', 'Sonja Kinski', 'Heath Freeman', 'Eric Roberts', 'Karen Austin']
0 Sex With Strangers []
5 Faith Like Potatoes ['Frank Rautenbach', 'Jeanne Neilson', 'Hamilton Dlamini', 'Sean Cameron Michael', 'Rochelle Buchan']
9 Beyond the Black Rainbow ['Michael Rogers', 'Scott Hylands', 'Marilyn Norry', 'Eva Allan', 'Rondel Reynoldson', 'Ryley Zinger', 'Gerry South', 'Chris Gauthier', 'Geoffrey Conder']
1 The Vatican Exorcisms ['Joe Marino']
7 Lake Mungo ['Talia Zucker', 'Rosie Traynor', 'David Pledger', 'Martin Sharpe', 'Steve Jodrell', 'Tamara Donnellan', 'Scott Terrill']
8 Rocket Singh: Salesman of the Year ['Ranbir Kapoor', 'Sumeet Darshan Dobhal', 'Gauhar Khan', 'Shazahn Padamsee', 'Prem Chopra', 'Naveen Kaushik', 'Mukesh Bhatt', 'Kyra Dutt']
7 Silent Running ['Bruce Dern', 'Cliff Potts', 'Ron Rifkin', 'Jesse Vint', 'Steven Brown', 'Mark Persons', 'Cheryl Sparks']
4 The Sleepwalker ['Christopher Abbott', 'Brady Corbet', 'Stephanie Ellis', 'Gitte Witt']
5 An Inconvenient Truth ['Al Gore', 'Billy West', 'Ronald Reagan', 'George W. Bush', 'George H. W. Bush']
6 Departure ['Juliet Stevenson', 'Alex Lawther', 'Phénix Brossard', 'Finbar Lynch', 'Niamh Cusack', 'Patrice Juiff']
5 Food, Inc. ['Michael Pollan', 'Eric Schlosser', 'Richard Lobb', 'Vince Edwards', 'Carole Morison']
4 October Baby ['Rachel Hendrix ', 'Jason Burkey', 'Robert Amaya ', 'John Schneider']
5 Next Stop Wonderland ['Hope Davis', 'Philip Seymour Hoffman', 'Holland Taylor', 'Alan Gelfant', 'Jason Lewis']
9 Frozen River ['Melissa Leo', 'Misty Upham', 'Charlie McDermott', 'John Canoe', 'Jay Klaitz', 'Dylan Carusona', 'James Reilly', "Michael O'Keefe", 'Mark Boone Junior']
5 Two Girls and a Guy ['Robert Downey Jr.', 'Natasha Gregson Wagner', 'Heather Graham', 'Angel David', 'Frederique van der Wal']
3 Who Killed the Electric Car? ['Martin Sheen', 'Mel Gibson', 'Tom Hanks']
4 Slam ['Saul Williams', 'Sonja Sohn', 'Bonz Malone', 'Beau Sia']
3 Brigham City ['Richard Dutcher', 'Matthew A. Brown', 'Wilford Brimley']
8 All the Real Girls ['Paul Schneider', 'Zooey Deschanel', 'Danny McBride', 'Maurice Compte', 'Heather McComb', 'Shea Whigham', 'Patricia Clarkson', 'Summer Shelton']
5 Dream with the Fishes ['David Arquette', 'Brad Hunt', 'Kathryn Erbe', 'Patrick McGaw', 'Cathy Moriarty']
8 The Battle of Shaker Heights ['Shia LaBeouf', 'Elden Henson', 'Amy Smart', 'Billy Kay', 'Kathleen Quinlan', 'Shiri Appleby', 'William Sadler', 'Ray Wise']
4 Taxi to the Dark Side ['Brian Keith Allen', 'Moazzam Begg', 'Christopher Beiring', 'Alex Gibney']
2 A LEGO Brickumentary ['Jason Bateman', 'Matthias Klie']
6 Hardflip ['Randy Wayne', 'John Schneider', 'Rosanna Arquette', 'Sean Michael Afable', 'Jason Dundas', 'Matthew Ziff']
8 Chocolate: Deep Dark Secrets ['Anil Kapoor', 'Sunil Shetty', 'Arshad Warsi', 'Emraan Hashmi', 'Irrfan Khan', 'Sushma Reddy', 'Tanushree Dutta', 'Emma Bunton']
9 The House of the Devil ['Jocelin Donahue', 'Mary Woronov', 'Greta Gerwig', 'AJ Bowen', 'Heather Robb', 'Darryl Nau', 'Brenda Cooney', 'Tom Noonan', 'Dee Wallace']
4 The Perfect Host ['David Hyde Pierce', 'Clayne Crawford', 'Nathaniel Parker', 'Helen Reddy']
7 The Last Big Thing ['Dan Zukovic', 'Mark Ruffalo', 'Sibel Ergener', 'James Lorinz', 'Yul Vazquez', 'Louis Mustillo', 'Blaine Capatch']
4 16 to Life ['Hallee Hirsh', 'Theresa Russell', 'Shiloh Fernandez', 'Will Rothhaar']
6 Alone With Her ['Colin Hanks', 'Ana Claudia Talancón', 'Jordana Spiro', 'Jonathon Trent', 'Alex Boling', 'Tony Armatrading']
8 Special ['Michael Rapaport', 'Josh Peck', 'Robert Baker', 'Jack Kehler', 'Alexandra Holden', 'Ian Bohen', 'Christopher Darga', 'Paul Blackthorne']
9 Sparkler ['Park Overall', 'Veronica Cartwright', 'Freddie Prinze Jr.', 'Don Harvey', 'Jamie Kennedy', 'Steven Petrarca', 'Grace Zabriskie', 'Octavia Spencer', 'Frances Bay']
0 The Helix... Loaded []
5 The Jimmy Show ['Frank Whaley', 'Carla Gugino', 'Ethan Hawke', 'Lynn Cohen', 'Jillian Stacom']
5 Heli ['Armando Espitia', 'Andrea Vergara', 'Linda Gonzalez', 'Juan Eduardo Palacios', 'Kenny Johnston']
4 Karachi se Lahore ['Shehzad Sheikh', 'Ayesha Omar', 'Yasir Hussain', 'Javed Sheikh']
3 Jimmy and Judy ['Edward Furlong', 'Rachael Bella', 'William Sadler']
7 Frat Party ['Randy Wayne', "Caroline D'Amore", 'Jareb Dauplaise', 'Lauren C. Mayhew', 'Dan Levy', 'Katerina Mikailenko', 'Robert Parks-Valletta']
3 Proud ['Vernel Bagneris', 'Marcus Chait', 'Michael Ciesla']
6 Childless ['Barbara Hershey', 'Joe Mantegna', 'Diane Venora', 'James Naughton', 'Natalie Dreyfuss', 'Jordan Baker']
4 Hidden Away ['Germán Alcarazu', 'Adil Koukouh', 'Ana Wagener', 'Alex Angulo']
5 My Last Day Without You ['Ken Duken', 'Nicole Beharie', 'Reg E. Cathey', 'Marlene Forte', 'Laith Nakli']
3 Steppin: The Movie ['Wesley Jonathan', 'Chrystee Pharris', 'Anthony Anderson']
7 Doc Holliday's Revenge ['Tom Berenger', 'Ashley Hayes', 'Eric Roberts', 'Bart Voitila', 'Oliver Rayon', 'Randy Jay Burrell', 'Daniel Dannas']
7 Black Rock ['Kate Bosworth', 'Lake Bell', 'Jay Paulson', 'Katie Aselton', 'Will Bouvier', 'Anslem Richardson', 'Carl K. Aselton III']
9 Truth or Dare ['Liam Boyle', 'Jack Gordon', 'Florence Hall', 'David Oakes', 'Jennie Jacques', 'Tom Kane', 'Jason Maza', 'David Sterne', 'Alexander Vlahos']
6 The Pet ['Pierre Dulat', 'Andrea Edmondson', 'Summer Nguyen', 'Lydia McLane', 'Steven Wollenberg', 'Magi Avila']
5 Zombie Hunter ['Martin Copping', 'Danny Trejo', 'Clare Niederpruem', 'Terry Guthrie', 'Jason Regier']
3 A Fine Step ['Luke Perry', 'Anna Claire Sneed', 'Leonor Varela']
8 Charly ['Cliff Robertson', 'Claire Bloom', 'Lilia Skala', 'Leon Janney', 'Ruth White', 'Dick Van Patten', 'Edward McNally', 'Barney Martin']
5 And Then Came Love ['Kevin Daniels', 'Michael Boatman', 'Jeremy Gumbs', 'Eartha Kitt', 'Vanessa Williams']
0 Food Chains []
6 The Horror Network Vol. 1 ['Nick Frangione', 'Artem Mishin', 'Jan Cornet', 'Brian Dorton', 'Javier Botet', 'Macarena Gómez']
5 Hard Candy ['Patrick Wilson', 'Ellen Page', 'Sandra Oh', 'Odessa Rae', 'G.J. Echternkamp']
7 Circumstance ['Nikohl Boosheri', 'Sarah Kazemy', 'Reza Sixo Safai', 'Soheil Parsa', 'Nasrin Pakkho', 'Sina Amedson', 'Keon Mohajeri']
6 The Hammer ['Adam Carolla', 'Oswaldo Castillo', 'Harold House Moore', 'Christopher Darga', 'Jonathan Hernandez', 'Heather Juergensen']
3 Elza ['Stana Roumillac', 'Vincent Byrd Le Sage', 'Christophe Cherki']
6 1982 ['Bokeem Woodbine', 'Sharon Leal', 'Wayne Brady', 'Quinton Aaron', 'Hill Harper', 'La La Anthony']
6 Time Changer ['D. David Morin', 'Gavin MacLeod', 'Hal Linden', "Jennifer O'Neill", 'Paul Rodríguez', 'Richard Riehle']
8 London to Brighton ['Georgia Groome', 'Johnny Harris', 'Sam Spruell', 'Lorraine Stanley', 'Alexander Morton', 'Nathan Constance', 'Jamie Kenna', 'Chloe Bale']
4 American Hero ['Stephen Dorff', 'Eddie Griffin', 'Bill Billions', 'Jonathan Billions']
4 Windsor Drive ['Samaire Armstrong', 'Anna Gurji', 'Matt Cohen', 'Kyan DuBois']
4 Crying with Laughter ['Stephen McCole', 'Malcolm Shields', 'Andrew Neil', 'Jo Hartley']
9 Ruby in Paradise ['Ashley Judd', 'Todd Field', 'Bentley Mitchum', 'Dorothy Lyman', 'Allison Dean', 'Betsy Douds', 'Felicia Hernández', 'Divya Satia', 'Bobby Barnes']
9 Raising Victor Vargas ['Victor Rasuk', 'Judy Marte', 'Melonie Diaz', 'Altagracia Guzman', 'Silvestre Rasuk', 'Krystal Rodriguez', 'Kevin Rivera', 'Wilfree Vasquez', 'Donna Maldonado']
6 Pandora's Box ['Louise Brooks', 'Fritz Kortner', 'Francis Lederer', 'Carl Goetz', 'Krafft-Raschig', 'Alice Roberts']
0 Harrison Montgomery []
5 Live-In Maid ['Norma Aleandro', 'Norma Argentina ', 'Marcos Mundstock', 'Claudia Lapacó', 'Elsa Berenguer']
6 The Mudge Boy ['Emile Hirsch', 'Tom Guiry', 'Richard Jenkins', 'Pablo Schreiber', 'Zachary Knighton', 'Ryan Donowho']
6 The Young Unknowns ['Devon Gummersall', 'Arly Jover', 'Eion Bailey', 'Leslie Bibb', 'Dale Godboldo', 'Simon Templeman']
5 Not Cool ['Shane Dawson', 'Cherami Leigh', 'Drew Monson', 'Michelle Veintimilla', 'Lisa Schwartz']
7 Vessel ['Brandon Bales', 'Brandy Maasch', 'Julie Mintz', 'Walter Phelan', 'Taylor Pigeon', 'Alan Pietruszewski', 'Whit Spurgeon']
1 Iraq for Sale: The War Profiteers ['Shereef Akeel']
7 Aqua Teen Hunger Force Colon Movie Film for Theaters ['Dana Snyder', 'Carey Means', 'Dave Willis', 'Andy Merrill', 'Bruce Campbell', 'Fred Armisen', 'Chris Kattan']
2 Kevin Hart: Laugh at My Pain ['Kevin Hart', "Na'im Lynn"]
8 The Innkeepers ['Sara Paxton', 'Pat Healy', 'Kelly McGillis', 'George Riddle', 'Lena Dunham', 'Alison Bartlett', 'Brenda Cooney', 'John Speredakos']
9 The Conformist ['Jean-Louis Trintignant', 'Stefania Sandrelli', 'Gastone Moschin', 'Dominique Sanda', 'Enzo Tarascio', 'Fosco Giachetti', 'José Quaglio', 'Pierre Clémenti', 'Yvonne Sanson']
6 Interview with the Assassin ['Dylan Haggerty', 'Renee Faia', 'Dennis Lau', 'Raymond J. Barry', 'Kelsey Kemper', 'Jared McVay']
7 Donkey Punch ['Nichola Burley', 'Sian Breckin', 'Jaime Winstone', 'Robert Boulter', 'Tom Burke', 'Julian Morris', 'Jay Taylor']
3 Hoop Dreams ['William Gates', 'Arthur Agee', 'Steve James']
8 Rize ['Christopher Toler', 'Tommy the Clown', 'Miss Prissy', 'Dragon', 'Ceasare Willis', 'La Niña', 'Larry Berry', 'Kevin Richardson']
9 L.I.E. ['Paul Dano', 'Bruce Altman', 'Brian Cox', 'Billy Kay', 'James Costa', 'Tony Michael Donnelly', 'Walter Masterson', 'Adam LeFevre', 'Chance Kelly']
7 B-Girl ["Julie 'Jules' Urich", 'Missy Yager', 'Wesley Jonathan', 'Drew Sidora', 'Aimee Garcia', 'James Martinez', 'Richard Yniguez']
6 Adulterers ['Sean Faris', 'Danielle Savre', 'Mehcad Brooks', 'Stephanie Charles', 'Steffinnie Phrommany', 'Rebecca Reaney']
8 Escape from Tomorrow ['Roy Abramsohn', 'Elena Schuber', 'Katelynn Rodriguez', 'Danielle Safady', 'Alison Lees-Taylor', 'Jack Dalton', 'Annet Mahendru', 'Lee Armstrong']
0 The Hadza:  Last of the First []
4 Treachery ['Matthew Ziff', 'Michael Biehn', 'Sarah Butler', 'Caitlin Keats']
8 Top Hat ['Fred Astaire', 'Ginger Rogers', 'Edward Everett Horton', 'Helen Broderick', 'Erik Rhodes', 'Eric Blore', 'Lucille Ball', 'Gino Corrado']
5 Mercy Streets ['Eric Roberts', 'David A.R. White', 'Cynthia Watros', 'Lawrence Taylor', 'Stacy Keach']
7 Carousel of Revenge ['Erik Allen', 'Randy Baranczyk', 'Chris Carlson', 'Ben Coler', 'Nancy Crocker', 'Jim Detmar', 'Crystal Donner']
5 They Will Have to Kill Us First ['Aliou Touré', 'Oumar Touré', 'Garba Touré', 'Nathanael Dembélé', 'Khaira Arby']
0 Light from the Darkroom []
0 The Harvest (La Cosecha) []
6 Love Letters ['Jamie Lee Curtis', 'Bonnie Bartlett', 'Matt Clark', 'James Keach', 'Amy Madigan', 'Sally Kirkland']
7 Juliet and Alfa Romeo ['Dario Nožić Serini', 'Jan Gerl Korenc', 'Špela Colja', 'Katja Škofić', 'Ana Dolinar', 'Andrej Nahtigal', 'Lena Capuder']
6 Open Water ['Blanchard Ryan', 'Daniel Travis', 'Saul Stein', 'Michael E. Williamson', 'Christina Zenato', 'John Charles']
0 Mad Hot Ballroom []
8 To Save A Life ['Randy Wayne', 'Deja Kreutzberg', 'Joshua Weigel', 'Steven Crowder', 'Kim Hidalgo', 'D. David Morin', 'Sean Michael Afable', 'Trinity Scott Brown']
9 Wordplay ['Will Shortz', 'Merl Reagle', 'Tyler Hinman', 'Trip Payne', 'Al Sanders', 'Ellen Ripstein', 'Jon Delfin', 'Bill Clinton', 'Jon Stewart']
6 The Singles Ward ['Will Swenson', 'Connie Young', 'Daryn Tufts', 'Michael Birkeland', 'Lincoln Hoppe', 'Kirby Heyborne']
4 Osama ['Marina Golbahari', 'Arif Herati', 'Zubaida Sahar', 'Mohammad Nadir Khwaja']
8 Sholem Aleichem: Laughing In The Darkness ['Rachel Dratch', 'Hillel Halkin', 'Jason Kravitz', 'Dan Miron', 'Peter Riegert', 'Alan Rosenberg', 'David Roskies', 'Ruth Wisse']
1 The R.M. ['Kirby Heyborne']
7 Twin Falls Idaho ['Mark Polish', 'Michael Polish', 'Michele Hicks', 'Jon Gries', 'Patrick Bauchau', 'Garrett Morris', 'Lesley Ann Warren']
7 Mean Creek ['Rory Culkin', 'Scott Mechlowicz', 'Trevor Morgan', 'Josh Peck', 'Ryan Kelley', 'Carly Schroeder', 'Branden Williams']
5 Hurricane Streets ['Brendan Sexton III', 'Antoine McLean', 'Mtume Gant', 'Carlo Alban', 'David Roland Frank']
7 Civil Brand ['LisaRaye McCoy', "N'Bushe Wright", 'Monica Calhoun', 'Clifton Powell', 'Yasiin Bey', 'Da Brat', 'Tichina Arnold']
5 Deceptive Practice: The Mysteries and Mentors of Ricky Jay ['Ricky Jay', 'Dick Cavett', 'Winston Simon', 'David Mamet', 'Persi Diaconis']
6 Johnny Suede ['Brad Pitt', 'Calvin Levels', 'Catherine Keener', 'Nick Cave', 'Alison Moir', 'Samuel L. Jackson']
2 Kiss the Bride ['Tori Spelling', 'Les Williams']
5 Monsters ['Whitney Able', 'Scoot McNairy', 'Annalee Jefferies', 'Kevon Kane', 'Fernando Lara']
6 The Living Wake ['Jesse Eisenberg', "Mike O'Connell", 'Jim Gaffigan', 'Ann Dowd', 'Colombe Jacobsen-Derstine', 'Eddie Pepitone']
7 Scott Walker: 30 Century Man ['Scott Walker', 'Damon Albarn', 'David Bowie', 'Jarvis Cocker', 'Marc Almond', 'Sting', 'Johnny Marr']
6 Everything Put Together ['Radha Mitchell', 'Megan Mullally', 'Catherine Lloyd Burns', 'Jacqueline Heinze', 'Alan Ruck', 'Octavia Spencer']
0 The Outrageous Sophie Tucker []
0 America Is Still the Place []
8 Subconscious ['Tim Abell', 'Naomi Brockwell', 'Aleisha Force', 'Tom Stedham', 'Cambridge Jones', 'Dominick Mancino', 'Peter Barry', 'Peter Barry']
7 Enter Nowhere ['Katherine Waterston', 'Scott Eastwood', 'Sara Paxton', 'Shaun Sipos', 'Christopher Denham', 'Jesse Perez', 'Leigh Lezark']
7 El Rey de Najayo ['Manny Pérez', 'Luz Garcia', 'Sergio Carlo', 'Juan Maria Almonte', 'Rafael Estephan', 'Socrates Montas', 'Omar Ramirez']
6 Fight to the Finish ['Jennifer Hale', 'Evan Hannemann', 'Tonya Kay', 'Anna Ross', 'Tamara Rey', 'Vincent De Paul']
4 The Sound and the Shadow ['Joseph E. Murray', 'Alex Anfanger', 'Rhomeyn Johnson', 'Mary Kate Wiles']
6 Born to Fly: Elizabeth Streb vs. Gravity ['Elizabeth Streb', 'Fabio Tavares', 'Sarah Callan', 'Jaclyn Carlson', 'Leonardo Giron', 'Felix Hess']
0 The Little Ponderosa Zoo []
0 Straight Out of Brooklyn []
0 Diamond Ruff []
7 Conversations with Other Women ['Helena Bonham Carter', 'Aaron Eckhart', 'Yury Tsykun', 'Brian Geraghty', 'Brianna Brown', 'Nora Zehetner', 'Olivia Wilde']
8 Mutual Friends ['Caitlin Fitzgerald', 'Cheyenne Jackson', 'Peter Scanavino', 'Michael Stahl-David', 'Christina Cole', 'Jennifer Lafleur', 'Ross Partridge', 'Annika Peterson']
0 Rise of the Entrepreneur: The Search for a Better Way []
6 Metropolitan ['Edward Clements', 'Chris Eigeman', 'Taylor Nichols', 'Carolyn Farina', 'Isabel Gillies', 'Dylan Hundley']
2 Roadside ['Ace Marrero', 'Katie Stegeman']
5 Paranormal Activity ['Katie Featherston', 'Micah Sloat', 'Mark Fredrichs', 'Amber Armstrong', 'Ashley Palmer']
9 Dogtown and Z-Boys ['Sean Penn', 'Jay Adams', 'Henry Rollins', 'Steve Caballero', 'Tony Hawk', 'Jeff Ament', 'Tony Alva', 'Jeff Ho', 'Jake Phelps']
8 Quinceañera ['Emily Rios', 'Jesse Garcia', 'Chalo González', 'David W. Ross', 'Ramiro Iniguez', 'Araceli Guzman-Rico', 'Jesus Castanos', 'Johnny Chavez']
0 Gory Gory Hallelujah []
5 Tarnation ['Renee Leblanc', 'Adolph Davis', 'Jonathan Caouette', 'Rosemary Davis', 'David Sanin Paz']
0 I Want Your Money []
8 Love in the Time of Monsters ['Kane Hodder', 'Doug Jones', 'Gena Shaw', 'Marissa Skell', 'Michael McShane', 'Shawn Weatherly', 'Hugo Armstrong', 'Heather Rae Young']
9 The Dark Hours ['Kate Greenhouse', 'Aidan Devine', 'Gordon Currie', 'Iris Graham', 'Dov Tiefenbach', 'David Calderisi', 'Jeff Seymour', 'Trevor Hayes', 'Bruce McFee']
0 Fabled []
5 Show Me ['Michelle Nolden', 'Katharine Isabelle', 'Kett Turton', 'Gabriel Hogan', 'Allegra Fulton']
8 Cries and Whispers ['Harriet Andersson', 'Ingrid Thulin', 'Kari Sylwan', 'Liv Ullmann', 'Erland Josephson', 'Henning Moritzen', 'Georg Årlin', 'Ingmar Bergman']
1 Censored Voices ['Amos Oz']
5 Murderball ['Joe Bishop', 'Keith Cavill', 'Andy Cohn', 'Scott Hogsett', 'Christopher Igoe']
3 51 Birch Street ['Carol Block', 'Doug Block', 'Ellen Block']
7 My Dog Tulip ['Christopher Plummer', 'Lynn Redgrave', 'Isabella Rossellini', 'Peter Gerety', 'Brian Murray', 'Paul Hecht', 'Euan Morton']
9 Dogtooth ['Hristos Passalis', 'Angeliki Papoulia', 'Mary Tsoni', 'Christos Stergioglou', 'Michele Valley', 'Anna Kalaitzidou', 'Steve Krikris', 'Sissy Petropoulou', 'Alexander Voulgaris']
1 Tupac: Resurrection ['Tupac Amaru Shakur']
3 Tumbleweeds ['Janet McTeer', 'Kimberly J. Brown', 'Jennifer Paige']
9 The Prophecy ['Christopher Walken', 'Elias Koteas', 'Virginia Madsen', 'Eric Stoltz', 'Adam Goldberg', 'Viggo Mortensen', 'Amanda Plummer', 'Shawn Nelson', 'Emily Conforto']
5 The Big Swap ['Mark Adams', 'Mark Caven', 'Allison Egan', 'Jackie Sawiris', 'Kevin Howarth']
4 Wendy and Lucy ['Michelle Williams', 'Will Patton', 'Will Oldham', 'John Robinson']
9 3 Backyards ['Edie Falco', 'Embeth Davidtz', 'Elias Koteas', 'Rachel Resheff', 'Kathryn Erbe', 'Danai Gurira', 'Dana Eskelson', 'Kathy Searle', 'Peyton List']
0 Sisters in Law []
0 Ayurveda: Art of Being []
6 First Love, Last Rites ['Giovanni Ribisi', 'Natasha Gregson Wagner', 'Donal Logue', 'Robert John Burke', 'Jeannetta Arnette', 'Eli Marienthal']
4 Fighting Tommy Riley ['J.P. Davis', 'Eddie Jones', 'Christina Chambers', 'Diane Tayler']
8 Royal Kill ['Pat Morita', 'Eric Roberts', 'Gail Kim', 'Lalaine', 'Alexander Wraith', 'Jeannie Crist', 'Nicole Brown', 'Darren Kendrick']
8 The Looking Glass ['Dorothy Tristan', 'Jace Casey', 'Jace Casey', 'Harry Musselwhite', 'Elizabeth Stenholt', 'Jeff Puckett', 'Dallas Tolentino', 'Grace Tarnow']
9 Bizarre ['Pierre Prieur', 'Adrian James', 'Raquel Nave', 'Rebekah Underhill', 'Charlie Himmelstein', 'Luc Bierme', 'Pier Richard', 'Freddy Morgan', 'Michael Glover']
0 Death Calls []
9 Chuck & Buck ['Mike White', 'Chris Weitz', 'Lupe Ontiveros', 'Maya Rudolph', 'Paul Weitz', 'Beth Colt', 'Mary Wigmore', 'Paul Sand', 'Pamela Gordon']
0 Amidst the Devil's Wings []
7 Cube ['Nicole de Boer', 'Nicky Guadagni', 'David Hewlett', 'Andrew Miller', 'Julian Richings', 'Wayne Robson', 'Maurice Dean Wint']
7 Love and Other Catastrophes ['Matt Day', 'Matthew Dyktynski', 'Alice Garner', "Frances O'Connor", 'Radha Mitchell', 'Suzi Dougherty', 'Kym Gyngell']
3 I Married a Strange Person! ['Charis Michelsen', 'Tom Larson', 'Richard Spore']
8 November ['Courteney Cox', 'James Le Gros', 'Michael Ealy', 'Nora Dunn', 'Nick Offerman', 'Anne Archer', 'Matthew Carey', 'Robert Wu']
4 Teeth and Blood ['Glenn Plummer', 'Michelle Van Der Water', 'Danielle Vega', 'Greg Eagles']
6 On the Outs ['Judy Marte', 'Paola Mendoza', 'Flaco Navaja', 'Dominic Colón', "Edward O'Blenis", 'Adepero Oduye']
4 Rust ['Corbin Bernsen', 'Frank Gallacher', 'Lloyd Warner', 'Audrey Lynn Tennent']
9 Butterfly ['Stacy Keach', 'Pia Zadora', 'Orson Welles', 'Ed McMahon', 'June Lockhart', 'Lois Nettleton', 'Edward Albert', 'James Franciscus', 'Stuart Whitman']
0 UnDivided []
2 The Frozen ['Brit Morgan', 'Noah Segan']
5 Little Big Top ['Sid Haig', 'Richard Riehle', 'Mel England', 'Jacob Zachar', 'Travis Betz']
3 Along the Roadside ['Michael Madsen', 'Iman Crosson', 'Lazar Ristovski']
3 Burn ['Donald Austin', 'Brendan "Doogie" Milewski', 'Dave Parnell']
0 Short Cut to Nirvana: Kumbh Mela []
4 The Grace Card ['Michael Joiner', 'Michael Higgenbottom', 'Louis Gossett, Jr.', 'Cindy Hodge']
9 Middle of Nowhere ['David Oyelowo', 'Maya Gilbert', 'Sharon Lawrence', 'Emayatzy Corinealdi', 'Dondre Whitfield', 'Omari Hardwick', 'Lorraine Toussaint', 'Andy Spencer', 'Edwina Findley Dickerson']
0 Call + Response []
4 Malevolence ['Samantha Dark', 'Heather Magee', 'Richard Glover', 'R. Brandon Johnson']
4 Reality Show ['Adam Rifkin', 'Kelley Menighan Hensley', 'Kendra Sue Waldman', 'Scott Anderson']
8 Super Hybrid ['Shannon Beckner', 'Oded Fehr', 'Ryan Kennedy', 'Adrien Dorval', 'Duncan Fisher', 'Josh Strait', 'Kent Nolan', 'Melanie Papalia']
4 American Beast ['Armin Habibovich', 'Victoria Lachelle', 'Livingston Oden', 'Taylor Scott Olson']
0 The Case of the Grinning Cat []
5 Ordet ['Birgitte Federspiel', 'Preben Lerdorff Rye', 'Henrik Malberg', 'Emil Hass Christensen', 'Ejner Federspiel']
0 The Trials Of Darryl Hunt []
7 Samantha: An American Girl Holiday ['Mia Farrow', 'AnnaSophia Robb', 'Olivia Ballantyne', 'Kelsey Lewis', 'Jordan Bridges', 'Rebecca Mader', 'Keir Gilchrist']
9 Yesterday Was a Lie ['Chase Masterson', 'John Newton', 'Kipleigh Brown', 'Mik Scriba', 'Nathan Mobley', 'Warren Davis', 'Megan Henning', 'Jennifer Slimko', 'Peter Mayhew']
8 Theresa Is a Mother ['Edie McClurg', 'C. Fraser Press', 'Richard Poe', 'Robert Turano', 'Matthew Gumley', 'Schuyler Press', 'Maeve Press', 'Amaya Press']
4 H. ['Robin Bartlett', 'Rebecca Dayan', 'Will Janowitz', 'Julian Gamble']
6 Archaeology of a Woman ['Sally Kirkland', 'Victoria Clark', 'James Murtaugh', 'Karl Geary', 'Mary Testa', 'Elaine Bromka']
3 Children of Heaven ['Mohammad Amir Naji', 'Amir Farrokh Hashemian', 'Bahare Seddiqi']
5 Weekend ['Tom Cullen', 'Chris New', 'Jonathan Race', 'Laura Freeman', 'Loreto Murray']
7 She's Gotta Have It ['Tracy Camilla Johns', 'Tommy Redmond Hicks', 'John Canada Terrell', 'Spike Lee', 'Raye Dowell', 'Joie Lee', 'S. Epatha Merkerson']
0 Butterfly Girl []
5 The World Is Mine ['Ana Maria Guran', 'Iulia Ciochina', 'Oana Rusu', 'Ana Vatamanu', 'Florin Hritcu']
6 The Woman Chaser ['Patrick Warburton', 'Eugene Roche', 'Ron Morgan', 'Emily Newman', 'Paul Malevich', 'Lynette Bennett']
6 The Horse Boy ['Simon Baron-Cohen', 'Temple Grandin', 'Roy Richard Grinker', 'Rowan Isaacson', 'Rupert Isaacson', 'Kristin Neff']
3 Heroes of Dirt ['Joel Moody', 'William Martinez', 'Vivienne VanHorn']
0 Antarctic Edge: 70° South []
0 Top Spin []
4 Roger & Me ['Michael Moore', 'Roger B. Smith', 'Rhonda Britton', 'Fred Ross']
9 An American in Hollywood ['J.D. Williams', 'Hassan Johnson', 'Anil Raman', 'Richard Carroll Jr.', 'Richard Carroll Jr.', 'Samantha Esteban', 'Amber Lee Ettinger', 'Silvestre Rasuk', 'Gregory Woo']
0 The Blood of My Brother: A Story of Death in Iraq []
6 Your Sister's Sister ['Mark Duplass', 'Emily Blunt', 'Rosemarie DeWitt', 'Mike Birbiglia', 'Kate Bayley', 'Jeanette Maus']
7 A Dog's Breakfast ['David Hewlett', 'Kate Hewlett', 'Paul McGillion', 'Christopher Judge', 'Rachel Luttrell', 'Amanda Byram', 'Michael Lenic']
3 The Work and The Story ['Kirby Heyborne', 'Christopher Robin Miller', 'Eric Artell']
5 Facing the Giants ['James Blackwell', 'Alex Kendrick', 'Shannen Fields', 'Chris WIllis', 'Tracy Goode']
9 The Mighty ['Sharon Stone', 'Elden Henson', 'Kieran Culkin', 'Gena Rowlands', 'Harry Dean Stanton', 'Meat Loaf', 'Jenifer Lewis', 'James Gandolfini', 'Gillian Anderson']
9 The Lost Skeleton of Cadavra ['Fay Masterson', 'Andrew Parks', 'Susan McConnell', 'Brian Howe', 'Jennifer Blaire', 'Dan Conroy', 'Robert Deveau', 'Darrin Reed', 'Larry Blamire']
9 Dude Where's My Dog? ['Gabriela Castillo', 'Trish Cook', 'Alexander G. Eckert', 'Kevin Farley', 'Dan Glenn', 'Kim Hamilton', 'Brandon Middleton', 'Janina Washington', 'Monti Washington']
4 Indie Game: The Movie ['Jonathan Blow', 'Phil Fish', 'Edmund McMillen', 'Tommy Refenes']
9 Straightheads ['Gillian Anderson', 'Danny Dyer', 'Adam Rayner', 'Antony Byrne', 'Anthony Calf', 'Ralph Brown', 'Steven Robertson', 'Gugu Mbatha-Raw', 'Francesca Fowler']
4 Echo Dr. ['Johnathan Hurley', 'Jordan Savage', 'Dane Bowman', 'Claire Gordon-Harper']
5 The Night Visitor ['Max von Sydow', 'Trevor Howard', 'Liv Ullmann', 'Per Oscarsson', 'Rupert Davies']
9 The Past Is a Grotesque Animal ['Dottie Alexander', 'Derek Almstead', 'David Barnes', 'Kevin Barnes', 'Nina Barnes', 'Janelle Monae', 'Solange Knowles', 'Susan Sarandon', 'Jon Brion']
0 Peace, Propaganda & the Promised Land []
6 20 Dates ['Myles Berkowitz', 'Tia Carrere', 'Elisabeth Wagner', 'Richard Arlook', 'Robert McKee', 'Elie Samaha']
7 Queen Crab ['Michelle Simone Miller', 'Kathryn Metz', 'A.J. DeLucia', 'Steve Diasparra', 'Danielle Donahue', 'Ken Van Sant', 'Rich Lounello']
6 The FP ['Jason Trost', 'Lee Valmassy', 'Art Hsu', 'Caitlyn Folley', 'Brandon Barrera', 'James DeBello']
8 Supporting Characters ['Alex Karpovsky', 'Tarik Lowe', 'Arielle Kebbel', 'Melonie Diaz', 'Kevin Corrigan', 'Sophia Takal', 'Mike Landry', 'Lena Dunham']
6 The Dirties ['Matt Johnson', 'Owen Williams', 'Krista Madison', 'Brandon Wickens', 'Jay McCarroll', 'Shailene Garnett']
5 Hayride ['Richard Tyson', 'Sherri Eakin', 'Jeremy Ivy', 'Jeremy Sande', 'Corlandos Scott ']
8 The Naked Ape ['Josh Wise', 'Chelse Swain', 'Sean Shanks', 'Amanda MacDonald', 'Corbin Bernsen', 'Tony LaThanh', 'Michael Jackson', 'Lydia Blanco Garza']
0 Counting []
6 The Call of Cthulhu ['Matt Foyer', 'John Bolen', 'Ralph Lucas', 'Chad Fifer', 'Susan Zucker', 'Kalafatic Poole']
0 Bending Steel []
3 Smiling Fish & Goat On Fire ['Derick Martini', 'Amy Hathaway', 'Steven Martini']
8 Dawn of the Crescent Moon ['Barry Corbin', 'Brooke Coleman', 'Kurt Cole', 'Brandon Smith', 'Alan Pietruszewski', 'Tracey Birdsall', 'Kerry Beyer', 'Michelle Ellen Jones']
8 Raymond Did It ['Kyle Hoskins', 'Elissa Dowling', 'Linda Cieslik', 'Steven Lee Edwards', 'Valerie Meachum', 'Jessica Palette', 'Patricia Raven', 'Lindsay Felton']
4 The Legend of God's Gun ['Robert Bones', 'Kirpatrick Thomas', 'Dave Koenig', 'Julie Patterson']
3 Mutual Appreciation ['Justin Rice', 'Rachel Clift', 'Andrew Bujalski']
5 Her Cry: La Llorona Investigation ['Nichole Ceballos', 'James Ezrin', 'Everardo Guzman', 'Parker Riggs', 'Gabrielle Santamauro']
9 Down Terrace ['Robert Hill', 'Robin Hill', 'Julia Deakin', 'David Schaal', 'Tony Way', 'Michael Smiley', 'Kerry Peacock', 'Mark Kempner', 'Gareth Tunley']
3 Pink Narcissus ['Bobby Kendall', 'Donald L. Brooks', 'Charles Ludlam']
5 In the Company of Men ['Aaron Eckhart', 'Stacy Edwards', 'Matt Malloy', 'Michael Martin', 'Mark Rector']
6 Manito ['Franky G', 'Leo Minaya', 'Manuel Cabral', 'Jessica Morales', 'Julissa Lopez', 'Hector Gonzalez']
2 Slacker ['Richard Linklater', 'Mark James']
5 Dutch Kills ['R.L. Mann', 'Tama Filianga', 'Mikaal Bates', 'Celestine Rae', 'Lodric D. Collins']
6 Dry Spell ['Suzi Lorraine', 'Jared Degado', 'Heather Dorff', 'Rachael Robbins', 'Kris Eivers', 'Travis Legge']
1 Flywheel ['Alex Kendrick']
3 The Puffy Chair ['Mark Duplass', 'Katie Aselton', 'Rhett Wilkins']
5 All Superheroes Must Die ['Jason Trost', 'Lucas Till', 'James Remar', 'Sophie Merkley', 'Nick Principe']
7 The Circle ['Nargess Mamizadeh', 'Maryiam Palvin Almani', 'Mojgan Faramarzi', 'Elham Saboktakin', 'Monir Arab', 'Maedeh Tahmasebi', 'Maryam Shayegan']
4 Tin Can Man ['Michael Parle', 'Emma Eliza Regan', "Patrick O'Donnell", 'Kreeta Taponen']
5 Sanctuary: Quite a Conundrum ['Sasha Ramos', 'Erin Cline', 'Emily Rogers', 'Anthony Rutowicz', 'Joe Coffey']
0 Cavite []
7 El Mariachi ['Carlos Gallardo', 'Jaime de Hoyos', 'Peter Marquardt', 'Reinol Martinez', 'Ramiro Gomez', 'Consuelo Gómez', 'Juan García']
5 Newlyweds ['Edward Burns', 'Kerry Bishé', 'Marsha Dietlein', 'Caitlin Fitzgerald', 'Daniella Pineda']
7 Signed, Sealed, Delivered ['Eric Mabius', 'Kristin Booth', 'Crystal Lowe', 'Geoff Gustafson', 'Benjamin Hollingsworth', 'Laci J Mailey', 'Daphne Zuniga']
5 Shanghai Calling ['Daniel Henney', 'Eliza Coupe', 'Bill Paxton', 'Alan Ruck', 'Zhu Shimao']
8 My Date with Drew ['Drew Barrymore', 'Brian Herzlinger', 'Corey Feldman', 'Eric Roberts', 'Griffin Dunne', 'Samuel L. Jackson', 'Matt LeBlanc', "Bill D'Elia"]






```

```python
# 원하는 필드 데이터만 뽑기
movie_credit[['cast', 'title', 'vote_average']]
```

| cast |                                             title |               vote_average |      |
| ---: | ------------------------------------------------: | -------------------------: | ---- |
| 4598 | [Lillian Gish, Mae Marsh, Robert Harron, F.A. ... |                Intolerance | 7.4  |
| 4667 | [John Gilbert, Renée Adorée, Hobart Bosworth, ... |             The Big Parade | 7.0  |
| 2644 | [Brigitte Helm, Alfred Abel, Gustav Fröhlich, ... |                 Metropolis | 8.0  |
| 4463 | [Louise Brooks, Fritz Kortner, Francis Lederer... |              Pandora's Box | 7.6  |
| 4600 | [Charles King, Anita Page, Bessie Love, Nacio ... |        The Broadway Melody | 5.0  |
|  ... |                                               ... |                        ... | ...  |
| 4726 | [Nate Parker, Armie Hammer, Aja Naomi King, Ja... |      The Birth of a Nation | 6.5  |
| 3307 | [Eddie Murphy, Britt Robertson, Natascha McElh... |                 Mr. Church | 7.0  |
| 3413 | [Dane DeHaan, Tatiana Maslany, Gordon Pinsent,... |      Two Lovers and a Bear | 6.8  |
| 4262 | [Roni Akurati, Brighton Sharbino, Jason Lee, A... |           Growing Up Smith | 7.4  |
| 4559 |                                                [] | America Is Still the Place | 0.0  |

4809 rows × 3 columns

```python
# vote_average 순으로 데이터를 정렬하기
movie_credit[['cast', 'title', 'vote_average']].sort_values(by='vote_average', ascending=False)
```

|      |                                              cast |                      title | vote_average |
| ---: | ------------------------------------------------: | -------------------------: | -----------: |
| 4668 | [Sid Haig, Richard Riehle, Mel England, Jacob ... |             Little Big Top |         10.0 |
| 4052 | [Breckin Meyer, Peter Facinelli, Eddie Mills, ... |      Dancer, Texas Pop. 81 |         10.0 |
| 4254 |                                                [] |      Me You and Five Bucks |         10.0 |
| 3524 | [Georgina Cates, Peter Ustinov, Prunella Scale... |           Stiff Upper Lips |         10.0 |
| 3999 |                                                [] |                  Sardaarji |          9.5 |
|  ... |                                               ... |                        ... |          ... |
| 4125 |                                                [] |     Hum To Mohabbat Karega |          0.0 |
| 4595 |                                                [] |                     Fabled |          0.0 |
| 4506 | [Erik Allen, Randy Baranczyk, Chris Carlson, B... |        Carousel of Revenge |          0.0 |
| 4058 | [Nicole Smolen, Kim Baldwin, Ariana Stephens, ... |                     8 Days |          0.0 |
| 4559 |                                                [] | America Is Still the Place |          0.0 |

4809 rows × 3 columns

```python
dataset = movie_credit[['cast', 'vote_average']]

dataset
```

|      |                                              cast | vote_average |
| ---: | ------------------------------------------------: | -----------: |
| 4598 | [Lillian Gish, Mae Marsh, Robert Harron, F.A. ... |          7.4 |
| 4667 | [John Gilbert, Renée Adorée, Hobart Bosworth, ... |          7.0 |
| 2644 | [Brigitte Helm, Alfred Abel, Gustav Fröhlich, ... |          8.0 |
| 4463 | [Louise Brooks, Fritz Kortner, Francis Lederer... |          7.6 |
| 4600 | [Charles King, Anita Page, Bessie Love, Nacio ... |          5.0 |
|  ... |                                               ... |          ... |
| 4726 | [Nate Parker, Armie Hammer, Aja Naomi King, Ja... |          6.5 |
| 3307 | [Eddie Murphy, Britt Robertson, Natascha McElh... |          7.0 |
| 3413 | [Dane DeHaan, Tatiana Maslany, Gordon Pinsent,... |          6.8 |
| 4262 | [Roni Akurati, Brighton Sharbino, Jason Lee, A... |          7.4 |
| 4559 |                                                [] |          0.0 |

4809 rows × 2 columns

```python
# cast_dict 딕셔너리 데이터 만들기, cast, cast출연 횟수, vote_average더하기
cast_dict = {}
for i in range(len(dataset)):
    for j in range(len(dataset['cast'][i])):
        if dataset['cast'][i][j] in cast_dict:
            cast_dict[dataset['cast'][i][j]][0] += 1
            cast_dict[dataset['cast'][i][j]][1] += dataset['vote_average'][i]
        else: 
            cast_dict[dataset['cast'][i][j]] = [0, 0]

print(cast_dict)
```

```
{'Sam Worthington': [7, 41.699999999999996], 'Zoe Saldana': [19, 123.60000000000001], 'Sigourney Weaver': [27, 164.60000000000005], 'Stephen Lang': [10, 57.9], 'Michelle Rodriguez': [9, 52.39999999999999], 'Giovanni Ribisi': [20, 123.8], 'Joel David Moore': [4, 23.400000000000002], 'CCH Pounder': [3, 18.9], 'Wes Studi': [6, 35.5], 'Laz Alonso': [8, 49.6], 'Johnny Depp': [35, 229.0], 'Orlando Bloom': [10, 70.5], 'Keira Knightley': [17, 116.0], 'Stellan Skarsgård': [20, 130.60000000000002], 'Chow Yun-fat': [8, 46.7], 'Bill Nighy': [24, 153.8], 'Geoffrey Rush': [20, 130.0], 'Jack Davenport': [5, 34.9], 'Kevin McNally': [12, 78.4], 'Tom Hollander': [9, 59.59999999999999], 'Daniel Craig': [16, 103.60000000000001], 'Christoph Waltz': [9, 58.9], 'Léa Seydoux': [0, 0], 'Ralph Fiennes': [24, 161.1], 'Monica Bellucci': [7, 44.3], 'Ben Whishaw': [8, 54.5], 'Naomie Harris': [7, 46.300000000000004], 'Dave Bautista': [5, 29.400000000000002], 'Andrew Scott': [2, 12.1], 'Rory Kinnear': [3, 21.3], 'Christian Bale': [25, 168.80000000000004], 'Michael Caine': [28, 181.10000000000002], 'Gary Oldman': [26, 170.19999999999996], 'Anne Hathaway': [23, 150.00000000000003], 'Tom Hardy': [13, 90.00000000000003], 'Marion Cotillard': [11, 74.0], 'Joseph Gordon-Levitt': [17, 112.3], 'Morgan Freeman': [45, 294.8999999999999], 'Cillian Murphy': [14, 92.89999999999998], 'Juno Temple': [8, 49.5], 'Taylor Kitsch': [5, 30.499999999999996], 'Lynn Collins': [4, 25.7], 'Samantha Morton': [12, 80.10000000000001], 'Willem Dafoe': [30, 196.9], 'Thomas Haden Church': [17, 102.4], 'Mark Strong': [17, 112.3], 'Ciarán Hinds': [21, 132.6], 'Dominic West': [11, 68.7], 'James Purefoy': [5, 28.6], 'Bryan Cranston': [12, 78.50000000000001], 'Tobey Maguire': [12, 79.5], 'Kirsten Dunst': [23, 148.00000000000003], 'James Franco': [24, 150.39999999999998], 'Topher Grace': [8, 47.1], 'Bryce Dallas Howard': [8, 52.300000000000004], 'Rosemary Harris': [3, 20.1], 'James Cromwell': [21, 137.59999999999997], 'J.K. Simmons': [23, 145.30000000000004], 'Theresa Russell': [3, 17.5], 'Zachary Levi': [3, 17.6], 'Mandy Moore': [12, 69.2], 'Donna Murphy': [6, 35.4], 'Ron Perlman': [21, 123.8], 'M.C. Gainey': [13, 71.30000000000001], 'Jeffrey Tambor': [17, 101.20000000000002], 'Brad Garrett': [8, 47.49999999999999], 'Paul F. Tompkins': [0, 0], 'Richard Kiel': [5, 32.4], 'Delaney Rose Stein': [0, 0], 'Robert Downey Jr.': [27, 174.70000000000005], 'Chris Hemsworth': [13, 82.10000000000001], 'Mark Ruffalo': [25, 167.5], 'Chris Evans': [16, 103.80000000000001], 'Scarlett Johansson': [27, 177.10000000000005], 'Jeremy Renner': [15, 100.0], 'James Spader': [9, 54.10000000000001], 'Samuel L. Jackson': [57, 358.90000000000003], 'Don Cheadle': [21, 137.5], 'Aaron Taylor-Johnson': [9, 58.800000000000004], 'Daniel Radcliffe': [9, 62.10000000000001], 'Rupert Grint': [7, 50.199999999999996], 'Emma Watson': [11, 74.79999999999998], 'Tom Felton': [9, 59.4], 'Michael Gambon': [19, 127.90000000000002], 'Jim Broadbent': [32, 208.39999999999998], 'Helena Bonham Carter': [21, 141.79999999999998], 'Robbie Coltrane': [14, 93.1], 'Maggie Smith': [15, 99.80000000000001], 'Alan Rickman': [14, 98.8], 'Ben Affleck': [26, 165.60000000000002], 'Henry Cavill': [5, 31.400000000000002], 'Gal Gadot': [3, 18.4], 'Amy Adams': [23, 150.0], 'Jesse Eisenberg': [15, 95.00000000000001], 'Diane Lane': [15, 95.7], 'Jeremy Irons': [13, 83.7], 'Laurence Fishburne': [28, 174.4], 'Holly Hunter': [10, 65.0], 'Scoot McNairy': [8, 50.7], 'Brandon Routh': [3, 17.8], 'Kevin Spacey': [22, 152.1], 'Kate Bosworth': [18, 107.9], 'James Marsden': [22, 131.0], 'Parker Posey': [15, 89.69999999999997], 'Frank Langella': [13, 80.39999999999999], 'Sam Huntington': [3, 16.5], 'Eva Marie Saint': [3, 17.4], 'Marlon Brando': [8, 56.400000000000006], 'Kal Penn': [11, 60.99999999999999], 'Olga Kurylenko': [7, 42.900000000000006], 'Mathieu Amalric': [5, 34.300000000000004], 'Judi Dench': [24, 153.8], 'Giancarlo Giannini': [3, 20.2], 'Gemma Arterton': [8, 48.3], 'Jeffrey Wright': [21, 132.2], 'David Harbour': [5, 33.5], 'Jesper Christensen': [5, 33.6], 'Anatole Taubman': [0, 0], 'Jonathan Pryce': [13, 84.2], 'Lee Arenberg': [1, 7.5], 'Mackenzie Crook': [5, 32.699999999999996], 'Armie Hammer': [6, 38.3], 'William Fichtner': [17, 102.7], 'James Badge Dale': [6, 40.8], 'Tom Wilkinson': [26, 169.50000000000003], 'Ruth Wilson': [2, 13.8], 'Barry Pepper': [15, 94.5], 'James Frain': [8, 49.099999999999994], 'Mason Cook': [1, 4.4], 'Michael Shannon': [21, 130.2], 'Kevin Costner': [24, 155.0], 'Russell Crowe': [23, 152.0], 'Antje Traue': [5, 30.5], 'Christopher Meloni': [7, 42.699999999999996], 'Jadin Gould': [0, 0], 'Ben Barnes': [5, 29.800000000000004], 'William Moseley': [1, 6.7], 'Anna Popplewell': [2, 12.8], 'Skandar Keynes': [2, 12.9], 'Georgie Henley': [3, 19.4], 'Sergio Castellitto': [0, 0], 'Alicia Borrachero': [0, 0], 'Peter Dinklage'
```

```python
# 데이터 행 열 바꾸기
data_table = pd.DataFrame.from_dict(cast_dict, orient='index', columns=['num', 'vote'])
```

```python
# 데이터셋의 index이름 설정하기
data_table['cast'] = data_table.index
data_table = data_table.set_index('cast')
data_table
```

|                num | vote |       |
| -----------------: | ---: | ----: |
|               cast |      |       |
|    Sam Worthington |    7 |  41.7 |
|        Zoe Saldana |   19 | 123.6 |
|   Sigourney Weaver |   27 | 164.6 |
|       Stephen Lang |   10 |  57.9 |
| Michelle Rodriguez |    9 |  52.4 |
|                ... |  ... |   ... |
|    Daniella Pineda |    0 |   0.0 |
|      Laci J Mailey |    0 |   0.0 |
|         Zhu Shimao |    0 |   0.0 |
|   Brian Herzlinger |    0 |   0.0 |
|        Bill D'Elia |    0 |   0.0 |

19021 rows × 2 columns

```python
# cast출연횟수 5회 이상과 vote가 0보다 큰 데이터를 만들기, 평균 데이터 만들기

table = data_table[(data_table['num'] > 4) & (data_table['vote'] > 0)]
table['mean'] = round(data_table['vote']/data_table['num'], 2)
table
```



|                num | vote |  mean |      |
| -----------------: | ---: | ----: | ---: |
|               cast |      |       |      |
|    Sam Worthington |    7 |  41.7 | 5.96 |
|        Zoe Saldana |   19 | 123.6 | 6.51 |
|   Sigourney Weaver |   27 | 164.6 | 6.10 |
|       Stephen Lang |   10 |  57.9 | 5.79 |
| Michelle Rodriguez |    9 |  52.4 | 5.82 |
|                ... |  ... |   ... |  ... |
|      Dave Sheridan |    6 |  32.8 | 5.47 |
|        Robert Shaw |    5 |  35.3 | 7.06 |
|     George W. Bush |    5 |  35.5 | 7.10 |
|     John Carradine |    5 |  31.2 | 6.24 |
|         John Wayne |    5 |  34.0 | 6.80 |

1652 rows × 3 columns

```python
# 평균으로 정렬
table.sort_values(by='mean', ascending=False)
```

|                num | vote | mean |      |
| -----------------: | ---: | ---: | ---: |
|               cast |      |      |      |
|  John Ratzenberger |    5 | 38.0 | 7.60 |
|        Kenny Baker |    6 | 44.8 | 7.47 |
|    Anthony Daniels |    5 | 36.9 | 7.38 |
|        Jack Lemmon |    5 | 36.8 | 7.36 |
|      Alec Guinness |    6 | 43.9 | 7.32 |
|                ... |  ... |  ... |  ... |
| Natasha Henstridge |    6 | 26.6 | 4.43 |
|        Robert Davi |    6 | 26.2 | 4.37 |
|     Joanna Cassidy |    5 | 20.5 | 4.10 |
|  Nicholas Turturro |    5 | 19.7 | 3.94 |
|     Paul Rodríguez |    5 | 19.4 | 3.88 |

1652 rows × 3 columns

```python
# vote로 정렬
table = table.sort_values(by='vote', ascending=False)
table
```

|               num | vote |  mean |      |
| ----------------: | ---: | ----: | ---: |
|              cast |      |       |      |
| Samuel L. Jackson |   57 | 358.9 | 6.30 |
|    Robert De Niro |   54 | 349.5 | 6.47 |
|    Morgan Freeman |   45 | 294.9 | 6.55 |
|        Matt Damon |   40 | 265.1 | 6.63 |
|      Bruce Willis |   41 | 257.0 | 6.27 |
|               ... |  ... |   ... |  ... |
|          Tony Cox |    5 |  22.8 | 4.56 |
|        Don Harvey |    5 |  22.2 | 4.44 |
|    Joanna Cassidy |    5 |  20.5 | 4.10 |
| Nicholas Turturro |    5 |  19.7 | 3.94 |
|    Paul Rodríguez |    5 |  19.4 | 3.88 |

1652 rows × 3 columns

```python
plt.xticks(rotation=70)
sns.barplot(x=table.index, y="vote", data=table, palette="Paired")
```



![image](https://user-images.githubusercontent.com/60081286/86017812-77099e80-ba5f-11ea-9b78-72aa2e93860b.png)