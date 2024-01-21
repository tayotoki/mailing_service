from .services.mailing_run_service import start_mailing


def start_mailing_crons():
    start_mailing()
