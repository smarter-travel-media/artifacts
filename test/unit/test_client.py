# -*- coding: utf-8 -*-

"""
"""

import mock
import pytest
import requests


@pytest.fixture
def http_client():
    from artificium.http import VersionApiClient
    return mock.Mock(spec=VersionApiClient)


class TestMavenArtifactoryClient(object):
    def test_get_version(self, http_client):
        from artificium.client import MavenArtifactoryClient, MavenArtifactoryClientConfig

        config = MavenArtifactoryClientConfig()
        config.base_url = 'https://www.example.com/artifactory'
        config.repo = 'libs-release'
        config.is_snapshot = False
        config.http_client = http_client

        maven_client = MavenArtifactoryClient(config)
        url = maven_client.get_version('com.example.users.service', 'jar', '1.2.3')
        assert ('https://www.example.com/artifactory/libs-release/' +
                'com/example/users/service/1.2.3/service-1.2.3.jar') == url

    def test_get_latest_version_snapshot(self, http_client):
        from artificium.client import MavenArtifactoryClient, MavenArtifactoryClientConfig

        http_client.get_most_recent_versions.return_value = [
            '1.3.0-SNAPSHOT', '1.2.1-SNAPSHOT', '1.1.0-SNAPSHOT']

        config = MavenArtifactoryClientConfig()
        config.base_url = 'https://www.example.com/artifactory'
        config.repo = 'libs-snapshot'
        config.is_snapshot = True
        config.http_client = http_client

        maven_client = MavenArtifactoryClient(config)
        url = maven_client.get_latest_version('com.example.users.service', 'jar')
        assert ('https://www.example.com/artifactory/libs-snapshot/' +
                'com/example/users/service/1.3.0-SNAPSHOT/service-1.3.0-SNAPSHOT.jar') == url

    def test_get_latest_version_snapshot_no_results(self, http_client):
        from artificium.client import MavenArtifactoryClient, MavenArtifactoryClientConfig
        from artificium.exceptions import NoMatchingVersionsError

        request = mock.Mock(spec=requests.Request)
        response = mock.Mock(spec=requests.Response)
        response.status_code = 404
        error = requests.HTTPError("Something bad", request=request, response=response)
        http_client.get_most_recent_versions.side_effect = error

        config = MavenArtifactoryClientConfig()
        config.base_url = 'https://www.example.com/artifactory'
        config.repo = 'libs-snapshot'
        config.is_snapshot = True
        config.http_client = http_client

        maven_client = MavenArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_version('com.example.users.service', 'war')

    def test_get_latest_version_release(self, http_client):
        from artificium.client import MavenArtifactoryClient, MavenArtifactoryClientConfig

        http_client.get_most_recent_release.return_value = '4.13.4'

        config = MavenArtifactoryClientConfig()
        config.base_url = 'https://www.example.com/artifactory'
        config.repo = 'libs-release'
        config.is_snapshot = False
        config.http_client = http_client

        maven_client = MavenArtifactoryClient(config)
        url = maven_client.get_latest_version('com.example.users.service', 'jar')
        assert ('https://www.example.com/artifactory/libs-release/' +
                'com/example/users/service/4.13.4/service-4.13.4.jar') == url

    def test_get_latest_version_release_no_results(self, http_client):
        from artificium.client import MavenArtifactoryClient, MavenArtifactoryClientConfig
        from artificium.exceptions import NoMatchingVersionsError

        request = mock.Mock(spec=requests.Request)
        response = mock.Mock(spec=requests.Response)
        response.status_code = 404
        error = requests.HTTPError("Something bad", request=request, response=response)
        http_client.get_most_recent_release.side_effect = error

        config = MavenArtifactoryClientConfig()
        config.base_url = 'https://www.example.com/artifactory'
        config.repo = 'libs-release'
        config.is_snapshot = False
        config.http_client = http_client

        maven_client = MavenArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_version('com.example.users.service', 'war')

    def test_get_latest_versions_snapshot(self, http_client):
        from artificium.client import MavenArtifactoryClient, MavenArtifactoryClientConfig

        http_client.get_most_recent_versions.return_value = [
            '1.3.0-SNAPSHOT', '1.2.1-SNAPSHOT', '1.1.0-SNAPSHOT']

        config = MavenArtifactoryClientConfig()
        config.base_url = 'https://www.example.com/artifactory'
        config.repo = 'libs-snapshot'
        config.is_snapshot = True
        config.http_client = http_client

        maven_client = MavenArtifactoryClient(config)
        urls = maven_client.get_latest_versions('com.example.users.service', 'war')
        expected = [
            'https://www.example.com/artifactory/libs-snapshot/com/example/users/service/1.3.0-SNAPSHOT/service-1.3.0-SNAPSHOT.war',
            'https://www.example.com/artifactory/libs-snapshot/com/example/users/service/1.2.1-SNAPSHOT/service-1.2.1-SNAPSHOT.war',
            'https://www.example.com/artifactory/libs-snapshot/com/example/users/service/1.1.0-SNAPSHOT/service-1.1.0-SNAPSHOT.war'
        ]

        assert expected == urls

    def test_get_latest_versions_snapshot_no_results(self, http_client):
        from artificium.client import MavenArtifactoryClient, MavenArtifactoryClientConfig
        from artificium.exceptions import NoMatchingVersionsError

        request = mock.Mock(spec=requests.Request)
        response = mock.Mock(spec=requests.Response)
        response.status_code = 404
        error = requests.HTTPError("Something bad", request=request, response=response)
        http_client.get_most_recent_versions.side_effect = error

        config = MavenArtifactoryClientConfig()
        config.base_url = 'https://www.example.com/artifactory'
        config.repo = 'libs-snapshot'
        config.is_snapshot = True
        config.http_client = http_client

        maven_client = MavenArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_versions('com.example.users.service', 'war')

    def test_get_latest_versions_snapshot_only_release_results(self, http_client):
        from artificium.client import MavenArtifactoryClient, MavenArtifactoryClientConfig
        from artificium.exceptions import NoMatchingVersionsError

        http_client.get_most_recent_versions.return_value = []

        config = MavenArtifactoryClientConfig()
        config.base_url = 'https://www.example.com/artifactory'
        config.repo = 'libs-snapshot'
        config.is_snapshot = True
        config.http_client = http_client

        maven_client = MavenArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_versions('com.example.users.service', 'war')

    def test_get_latest_versions_release(self, http_client):
        from artificium.client import MavenArtifactoryClient, MavenArtifactoryClientConfig

        http_client.get_most_recent_versions.return_value = ['1.2.1', '1.2.0', '1.1.1']

        config = MavenArtifactoryClientConfig()
        config.base_url = 'https://www.example.com/artifactory'
        config.repo = 'libs-release'
        config.is_snapshot = False
        config.http_client = http_client

        maven_client = MavenArtifactoryClient(config)
        urls = maven_client.get_latest_versions('com.example.users.service', 'war')
        expected = [
            'https://www.example.com/artifactory/libs-release/com/example/users/service/1.2.1/service-1.2.1.war',
            'https://www.example.com/artifactory/libs-release/com/example/users/service/1.2.0/service-1.2.0.war',
            'https://www.example.com/artifactory/libs-release/com/example/users/service/1.1.1/service-1.1.1.war'
        ]

        assert expected == urls

    def test_get_latest_versions_release_no_results(self, http_client):
        from artificium.client import MavenArtifactoryClient, MavenArtifactoryClientConfig
        from artificium.exceptions import NoMatchingVersionsError

        request = mock.Mock(spec=requests.Request)
        response = mock.Mock(spec=requests.Response)
        response.status_code = 404
        error = requests.HTTPError("Something bad", request=request, response=response)
        http_client.get_most_recent_versions.side_effect = error

        config = MavenArtifactoryClientConfig()
        config.base_url = 'https://www.example.com/artifactory'
        config.repo = 'libs-release'
        config.is_snapshot = False
        config.http_client = http_client

        maven_client = MavenArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_versions('com.example.users.service', 'war')

    def test_get_latest_versions_release_only_snapshot_results(self, http_client):
        from artificium.client import MavenArtifactoryClient, MavenArtifactoryClientConfig
        from artificium.exceptions import NoMatchingVersionsError

        http_client.get_most_recent_versions.return_value = []

        config = MavenArtifactoryClientConfig()
        config.base_url = 'https://www.example.com/artifactory'
        config.repo = 'libs-release'
        config.is_snapshot = False
        config.http_client = http_client

        maven_client = MavenArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_versions('com.example.users.service', 'war')


class TestMavenArtifactUrlGenerator(object):
    def test_get_version_url_with_descriptor(self):
        from artificium.client import _MavenArtifactUrlGenerator
        gen = _MavenArtifactUrlGenerator('https://corp.example.com/artifactory', 'libs-release-local')
        url = gen.get_version_url('com.example.services', 'locations', 'jar', '4.5.1', 'sources')

        assert ('https://corp.example.com/artifactory/libs-release-local/' +
                'com/example/services/locations/4.5.1/locations-4.5.1-sources.jar') == url

    def test_get_version_url_without_descriptor(self):
        from artificium.client import _MavenArtifactUrlGenerator
        gen = _MavenArtifactUrlGenerator('https://corp.example.com/artifactory', 'libs-release-local')
        url = gen.get_version_url('com.example.services', 'locations', 'war', '4.5.1', None)

        assert ('https://corp.example.com/artifactory/libs-release-local/' +
                'com/example/services/locations/4.5.1/locations-4.5.1.war') == url
