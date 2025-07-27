import json
from items import ImdbMovieItem, ImdbActorItem

def extract_movies_data(json_data_movies):
    import json
    try:
        data = json.loads(json_data_movies)
        edges = (
            data.get('props', {})
                .get('pageProps', {})
                .get('pageData', {})
                .get('chartTitles', {})
                .get('edges', [])
        )
        if not isinstance(edges, list):
            raise ValueError('Path props > pageData > chartTitles > edges is not a list.')
        movies_ids = []
        for edge in edges:
            node = edge.get('node', {})
            movie_id = node.get('id')
            movies_ids.append(movie_id)
        return movies_ids
    except Exception as e:
        raise ValueError(f'Error parsing movies JSON: {e}')

def extract_next_data_json(response, detail=False, movie_id=None):
    next_data_json = response.xpath('//script[@id="__NEXT_DATA__" and @type="application/json"]/text()').get()
    if next_data_json is None:
        if detail and movie_id:
            msg = f'Tag <script id="__NEXT_DATA__" type="application/json"> not found on detail page for {movie_id}.'
        else:
            msg = 'Tag <script id="__NEXT_DATA__" type="application/json"> not found on the page.'
        raise ValueError(msg)
    return next_data_json

def extract_movie_item(detail_data):
    foldData = detail_data.get('props', {}).get('pageProps', {}).get('aboveTheFoldData', {})
    metacritic = foldData.get('metacritic') or {}
    metascore_obj = metacritic.get('metascore') if isinstance(metacritic, dict) else None
    metascore = metascore_obj.get('score') if isinstance(metascore_obj, dict) else None
    movie_item = ImdbMovieItem(
        movie_id=foldData.get('id'),
        title=foldData.get('originalTitleText', {}).get('text'),
        year=foldData.get('releaseDate', {}).get('year'),
        rating=foldData.get('ratingsSummary', {}).get('aggregateRating'),
        duration=get_duration_minutes(foldData.get('runtime', {}).get('seconds')),
        metascore=metascore
    )
    yield movie_item

def extract_actor_items(detail_data):
    mainColumnData = detail_data.get('props', {}).get('pageProps', {}).get('mainColumnData', {})
    foldData = detail_data.get('props', {}).get('pageProps', {}).get('aboveTheFoldData', {})
    main_actor_ids = extract_main_actors(foldData)
    cast_edges = mainColumnData.get('cast', {}).get('edges', [])
    for edge in cast_edges:
        node = edge.get('node', {})
        actor = node.get('name', {})
        actor_id = actor.get('id')
        actor_name = actor.get('nameText', {}).get('text')
        if actor_id and actor_name:
            yield ImdbActorItem(
                actor_id=actor_id,
                movie_id=foldData.get('id'),
                name=actor_name,
                isMainCharacter=actor_id in main_actor_ids
            )

def extract_main_actors(foldData):
    cast_page_edges = foldData.get('castPageTitle', {}).get('edges', [])
    main_actor_ids = set()
    for edge in cast_page_edges:
        node = edge.get('node', {})
        actor = node.get('name', {})
        actor_id = actor.get('id')
        if actor_id:
            main_actor_ids.add(actor_id)
    return main_actor_ids

def get_duration_minutes(seconds):
    try:
        if isinstance(seconds, int) and seconds % 60 == 0:
            return seconds // 60
        else:
            return 0
    except Exception:
        return 0
