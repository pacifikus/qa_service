import logging
import pickle
from pathlib import Path

import click
import pandas_read_xml as pdx
import tensorflow_hub as hub
import yaml


def load_model(model_path):
    """
    The load_model function loads a pre-trained model from the specified path.

    :param model_path: Specify the location of the model that will be loaded
    :return: A model that can be used for predictions
    """
    return hub.load(model_path)


def read_posts(posts_filepath):
    """
    The read_posts function reads the posts.xml file and returns a dataframe with three columns:
        post_type_id, title, id. The function only keeps rows where post_type_id is equal to 1.

    :param posts_filepath: Specify the filepath to the posts
    :return: A dataframe with three columns: post_type_id, title, and id
    """
    posts_df = pdx.read_xml(posts_filepath, ['posts', 'row'])
    posts_df = posts_df.T
    posts_df['post_type_id'] = posts_df[0].apply(lambda x: x.get('@PostTypeId'))
    posts_df['title'] = posts_df[0].apply(lambda x: x.get('@Title'))
    posts_df['id'] = posts_df[0].apply(lambda x: x.get('@Id'))
    posts_df = posts_df[posts_df['post_type_id'] == '1']
    return posts_df[['post_type_id', 'title', 'id']]


def save_embeddings(embeddings_filepath, embeddings):
    """
    The save_embeddings function saves the embeddings to a pickle file.

    :param embeddings_filepath: Specify the path to where the embeddings will be saved
    :param embeddings: Embeddings to save in a pickle file
    """
    with open(embeddings_filepath, mode='wb') as f:
        pickle.dump(embeddings, f)


def pack_embeddings_with_data(embeddings, posts):
    """
    The pack_embeddings_with_data function takes in a list of embeddings and a dataframe of posts.
    It returns a list of tuples, where each tuple contains the post id, title, and embedding.

    :param embeddings: Embeddings for posts
    :param posts: Dataframe with title and id of each post
    :return: A list of tuples, where each tuple contains the index, title and embedding for a post
    """
    res = []
    for i, embedding in enumerate(embeddings):
        idx, title = int(posts.iloc[i]['id']), posts.iloc[i]['title']
        res.append((idx, title, embedding))
    return res


@click.command()
@click.option(
    "-cf",
    "--config_path",
    type=click.Path(exists=True),
    help="Path to config file",
    required=True,
)
def compute_embeddings(config_path):
    """
    The compute_embeddings function computes the embeddings for a given dataset of post titles.
    It loads the model from a file, and uses it to compute embeddings for each title in the dataset.
    The resulting embeddings are then saved to .pkl file.

    :param config_path: Specify the path to the yaml configuration file
    """
    with open(config_path) as conf_file:
        config = yaml.safe_load(conf_file)

    posts_filename = config['data']['posts_filename']
    posts_filepath = Path(config['data']['so_dataset_path']) / posts_filename
    posts = read_posts(posts_filepath)
    logger.info("Post titles has been read...")

    model = load_model(config['model']['model_path'])
    logger.info("Model has been loaded...")

    embeddings = model(posts['title'])
    logger.info("Embeddings have been computed...")

    embeddings = pack_embeddings_with_data(embeddings, posts)
    embeddings_filepath = Path(config['data']['processed_path']) / config['data']['embeddings_filename']
    save_embeddings(embeddings_filepath, embeddings)
    logger.info(f"Embeddings have been saved to {embeddings_filepath}...")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)
    compute_embeddings()
