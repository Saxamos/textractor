import subprocess
from subprocess import call

import click

from prospectus_field_extraction import ROOT_PATH
from prospectus_field_extraction.data.script import scrap_share_information, build_fund_name_dataset
from prospectus_field_extraction.model.lookup import (classification_finder, benchmark_finder, inception_date_finder,
                                                      closing_date_finder, depositary_finder, goal_finder, isin_finder)
from prospectus_field_extraction.model.ner import train_ner, test_ner

LOOKUP_COMMANDS = {'benchmark': benchmark_finder,
                   'classification': classification_finder,
                   'inception_date': inception_date_finder,
                   'closing_date': closing_date_finder,
                   'depositary': depositary_finder,
                   'goal': goal_finder,
                   'isin': isin_finder}


@click.group()
def main():
    pass


@main.command(help='Download and preprocess data.')
def download():
    call((ROOT_PATH / 'data' / 'script' / 'scrap_list_of_fund.sh').as_posix())
    call((ROOT_PATH / 'data' / 'script' / 'scrap_pdf.sh').as_posix())
    scrap_share_information.main()
    call((ROOT_PATH / 'data' / 'script' / 'transform_pdf_to_text.sh').as_posix())
    build_fund_name_dataset.main()


@main.command(help='Compute the lookup model accuracy on one field.')
@click.argument('command', type=click.Choice(LOOKUP_COMMANDS.keys()))
def lookup(command):
    LOOKUP_COMMANDS[command].main()


@main.command(help='Train or test the NER model.')
@click.argument('mode', type=click.Choice(['train', 'test']))
@click.option('--n-iter-train', default=15, type=click.INT, help='Number of training iterations in train mode.')
@click.option('--model-dir-test', default='ckpt', type=click.Path(), help='Number of training iterations in test mode.')
@click.option('--verbosity-test', default='2', type=click.Choice(['0', '1', '2']), help='Verbosity level in test mode.')
def ner(mode, n_iter_train, model_dir_test, verbosity_test):
    if mode == 'train':
        train_ner.main(n_iter_train)
    else:
        test_ner.main(model_dir_test, int(verbosity_test))


@main.command(help='Launch the streamlit application.')
def app():
    subprocess.check_output(['streamlit', 'run', (ROOT_PATH / 'app' / 'streamlit_app.py').as_posix()])


if __name__ == '__main__':
    main()
