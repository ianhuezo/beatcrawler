import pytest
from beatcrawler.crawler import  write_song_ids_to_file, get_all_page_ids

@pytest.mark.skip(reason="need to make folder for this")
def test_song_id_retrieval_writes_to_file():
    user_id = '76561198046220364'
    save_path = './song_ids/truffledore_ids.csv'
    write_song_ids_to_file(user_id, save_path)
    with open(save_path, "r") as f:
        assert len(f.readlines()) == 8

def test_get_all_page_ids():
    user_id = '76561198046220364'
    scoresaber_url = f'https://scoresaber.com/u/{user_id}'
    page_ids = get_all_page_ids(scoresaber_url, page_max=1)
    assert len(page_ids) == 8