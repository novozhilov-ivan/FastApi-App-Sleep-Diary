from functools import lru_cache

from dishka import Container, make_container
from dishka.integrations.fastapi import FastapiProvider

from src.domain.sleep_diary.providers import DomainSleepDiaryProvider
from src.gateways.postgresql.providers import DatabaseProvider, TestDatabaseProvider
from src.infra.application.pages.providers import InfraApplicationPagesProvider
from src.infra.identity.providers import InfraIdentityProvider
from src.infra.sleep_diary.providers import InfraSleepDiaryProvider
from src.project.settings import Config
from src.project.settings.providers import SettingsProvider

config = Config()


@lru_cache(1)
def get_container() -> Container:
    return make_container(
        InfraIdentityProvider(),
        InfraApplicationPagesProvider(),
        InfraSleepDiaryProvider(),
        DomainSleepDiaryProvider(),
        DatabaseProvider(),
        SettingsProvider(),
        FastapiProvider(),
        context={Config: config},
    )


@lru_cache(1)
def get_test_container() -> Container:
    return make_container(
        InfraIdentityProvider(),
        InfraSleepDiaryProvider(),
        DomainSleepDiaryProvider(),
        TestDatabaseProvider(),
        SettingsProvider(),
        FastapiProvider(),
        context={Config: config},
    )
