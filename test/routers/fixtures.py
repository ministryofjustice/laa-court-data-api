import datetime as dt

import pytest
import respx
from httpx import Response

from laa_court_data_api_app.config.court_data_adaptor import CdaSettings
from laa_court_data_api_app.models.hearing.hearing import Hearing
from laa_court_data_api_app.models.hearing.hearing_result import HearingResult
from laa_court_data_api_app.models.prosecution_cases.defendant_summary import DefendantSummary
from laa_court_data_api_app.models.hearing_summaries.hearing_summary import HearingSummary
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases import ProsecutionCases
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases_results import ProsecutionCasesResults
from laa_court_data_api_app.models.token_response import TokenResponse


@pytest.fixture()
def override_get_cda_settings():
    return CdaSettings(cda_secret="12345", cda_uid="12345", cda_endpoint="http://test-url/")


@pytest.fixture()
def get_new_token_response():
    token = "12345"
    created_at = dt.datetime.utcnow() - dt.datetime(1970, 1, 1)
    return TokenResponse(access_token=token, token_type="Bearer", expires_in=300,
                         created_at=int(created_at.total_seconds()))


@pytest.fixture()
def get_prosecution_case_results():
    return ProsecutionCasesResults(total_results=1,
                                   results=[ProsecutionCases(hearing_summaries=[HearingSummary(hearing_type="test")],
                                                             defendant_summaries=[DefendantSummary(name="test")])])


@pytest.fixture()
def get_hearing_results():
    return HearingResult(hearing=Hearing(jurisdiction_type="test"))


@pytest.fixture()
def mock_cda_client(get_new_token_response, get_prosecution_case_results, get_hearing_results):
    with respx.mock(assert_all_called=False) as respx_mock:
        get_route = respx_mock.post("http://test-url/oauth/token", name="token_endpoint")
        get_route.return_value = Response(200, json=get_new_token_response.dict())

        failed_token_route = respx_mock.post("http://failed-test-url/oauth/token", name="failed_token_endpoint")
        failed_token_route.return_value = Response(500)

        pass_route = respx_mock.get("http://test-url/api/internal/v2/prosecution_cases",
                                    params={"filter[prosecution_case_reference]": "pass"}, name="pass_route")
        pass_route.return_value = Response(200, json=get_prosecution_case_results.dict())
        fail_route = respx_mock.get("http://test-url/api/internal/v2/prosecution_cases",
                                    params={"filter[prosecution_case_reference]": "fail"}, name="fail_route")
        fail_route.return_value = Response(400)
        notfound_route = respx_mock.get("http://test-url/api/internal/v2/prosecution_cases",
                                        params={"filter[prosecution_case_reference]": "notfound"},
                                        name="notfound_route")
        notfound_route.return_value = Response(404)
        exception_route = respx_mock.get("http://test-url/api/internal/v2/prosecution_cases",
                                         params={"filter[prosecution_case_reference]": "exception"},
                                         name="exception_route")
        exception_route.return_value = Response(500)

        # /defendants by name and date of birth
        pass_name_dob_route = respx_mock.get("http://test-url/api/internal/v2/prosecution_cases",
                                             params={"filter[name]": "pass", "filter[date_of_birth]": "pass"},
                                             name="pass_name_dob_route")
        pass_name_dob_route.return_value = Response(200, json=get_prosecution_case_results.dict())
        fail_name_dob_route = respx_mock.get("http://test-url/api/internal/v2/prosecution_cases",
                                             params={"filter[name]": "fail", "filter[date_of_birth]": "fail"},
                                             name="fail_name_dob_route")
        fail_name_dob_route.return_value = Response(400)
        notfound_name_dob_route = respx_mock.get("http://test-url/api/internal/v2/prosecution_cases",
                                                 params={"filter[name]": "notfound",
                                                         "filter[date_of_birth]": "notfound"},
                                                 name="notfound_name_dob_route")
        notfound_name_dob_route.return_value = Response(404)
        exception_name_dob_route = respx_mock.get("http://test-url/api/internal/v2/prosecution_cases",
                                                  params={"filter[name]": "exception",
                                                          "filter[date_of_birth]": "exception"},
                                                  name="exception_name_dob_route")
        exception_name_dob_route.return_value = Response(500)

        # /defendants by urn and uuid
        pass_urn_uuid_route = respx_mock.get(
            "http://test-url/api/internal/v2/prosecution_cases/pass/defendants/22d2222c-22ff-22ec-b222-2222ac222222",
            name="pass_urn_uuid_route")
        pass_urn_uuid_route.return_value = Response(200, json=get_prosecution_case_results.dict())

        fail_urn_uuid_route = respx_mock.get(
            "http://test-url/api/internal/v2/prosecution_cases/fail/defendants/22d2222c-22ff-22ec-b222-2222ac222222",
            name="fail_urn_uuid_route")
        fail_urn_uuid_route.return_value = Response(400)

        notfound_urn_uuid_route = respx_mock.get(
            "http://test-url/api/internal/v2/prosecution_cases/404/defendants/22d2222c-22ff-22ec-b222-2222ac222222",
            name="notfound_urn_uuid_route"
        )
        notfound_urn_uuid_route.return_value = Response(404)

        exception_urn_uuid_route = respx_mock.get(
            "http://test-url/api/internal/v2/prosecution_cases/error/defendants/22d2222c-22ff-22ec-b222-2222ac222222",
            name="exception_urn_uuid_route")
        exception_urn_uuid_route.return_value = Response(500)

        # /hearing
        pass_hearing_route = respx_mock.get(
            "http://test-url/api/internal/v2/hearing_results/00d0000c-00ff-00ec-b000-0000ac000000",
            name="pass_hearing_route")
        pass_hearing_route.return_value = Response(200, json=get_hearing_results.dict())
        fail_hearing_route = respx_mock.get(
            "http://test-url/api/internal/v2/hearing_results/00d0000c-00ff-00ec-b000-0000ac000001",
            name="fail_hearing_route")
        fail_hearing_route.return_value = Response(400)
        notfound_hearing_route = respx_mock.get(
            "http://test-url/api/internal/v2/hearing_results/00d0000c-00ff-00ec-b000-0000ac000002",
            name="notfound_hearing_route")
        notfound_hearing_route.return_value = Response(404)
        exception_hearing_route = respx_mock.get(
            "http://test-url/api/internal/v2/hearing_results/00d0000c-00ff-00ec-b000-0000ac000003",
            name="exception_hearing_route")
        exception_hearing_route.return_value = Response(500)

        yield respx_mock
