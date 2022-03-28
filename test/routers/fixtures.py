import datetime as dt

import pytest
import respx
from httpx import Response

from laa_court_data_api_app.config.court_data_adaptor import CdaSettings
from laa_court_data_api_app.models.hearing.hearing import Hearing
from laa_court_data_api_app.models.hearing.hearing_result import HearingResult
from laa_court_data_api_app.models.hearing_events.hearing_events_result import HearingEventsResult
from laa_court_data_api_app.models.hearing_summaries.hearing_summary import HearingSummary
from laa_court_data_api_app.models.laa_references.external.request.laa_references_patch_request import \
    LaaReferencesPatchRequest
from laa_court_data_api_app.models.laa_references.internal.request.laa_references_patch import LaaReferencesPatch
from laa_court_data_api_app.models.prosecution_cases.defendant_summary import DefendantSummary
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
def get_hearing_events_results():
    return HearingEventsResult(has_active_hearing=True, events=[])


@pytest.fixture()
def get_hearing_results():
    return HearingResult(hearing=Hearing(jurisdiction_type="test"))


@pytest.fixture()
def mock_cda_client(get_new_token_response, get_prosecution_case_results,
                    get_hearing_results, get_hearing_events_results):
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

        pass_asn_route = respx_mock.get(
            "http://test-url/api/internal/v2/prosecution_cases",
            params={"filter[arrest_summons_number]": "pass"},
            name="pass_asn_route")
        pass_asn_route.return_value = Response(200, json=get_prosecution_case_results.dict())

        fail_asn_route = respx_mock.get(
            "http://test-url/api/internal/v2/prosecution_cases",
            params={"filter[arrest_summons_number]": "fail"},
            name="fail_asn_route")
        fail_asn_route.return_value = Response(400)

        notfound_asn_route = respx_mock.get(
            "http://test-url/api/internal/v2/prosecution_cases",
            params={"filter[arrest_summons_number]": "notfound"},
            name="notfound_asn_route"
        )
        notfound_asn_route.return_value = Response(404)

        exception_asn_route = respx_mock.get(
            "http://test-url/api/internal/v2/prosecution_cases",
            params={"filter[arrest_summons_number]": "exception"},
            name="exception_asn_route")
        exception_asn_route.return_value = Response(500)

        pass_nino_route = respx_mock.get(
            "http://test-url/api/internal/v2/prosecution_cases",
            params={"filter[national_insurance_number]": "pass"},
            name="pass_nino_route")
        pass_nino_route.return_value = Response(200, json=get_prosecution_case_results.dict())

        fail_nino_route = respx_mock.get(
            "http://test-url/api/internal/v2/prosecution_cases",
            params={"filter[national_insurance_number]": "fail"},
            name="fail_nino_route")
        fail_nino_route.return_value = Response(400)

        notfound_nino_route = respx_mock.get(
            "http://test-url/api/internal/v2/prosecution_cases",
            params={"filter[national_insurance_number]": "notfound"},
            name="notfound_nino_route"
        )
        notfound_nino_route.return_value = Response(404)

        exception_nino_route = respx_mock.get(
            "http://test-url/api/internal/v2/prosecution_cases",
            params={"filter[national_insurance_number]": "exception"},
            name="exception_nino_route")
        exception_nino_route.return_value = Response(500)

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

        # /hearing_events by date
        hearing_events_pass = respx_mock.get(
            "http://test-url/api/internal/v2/hearings/22d2222c-22ff-22ec-b222-2222ac222222/event_log/pass",
            name="pass_hearing_events_route")
        hearing_events_pass.return_value = Response(200, json=get_hearing_events_results.dict())

        fail_hearing_events_uuid_route = respx_mock.get(
            "http://test-url/api/internal/v2/hearings/22d2222c-22ff-22ec-b222-2222ac222222/event_log/fail",
            name="fail_hearing_events_route")
        fail_hearing_events_uuid_route.return_value = Response(400)

        notfound_hearing_events_uuid_route = respx_mock.get(
            "http://test-url/api/internal/v2/hearings/22d2222c-22ff-22ec-b222-2222ac222222/event_log/notfound",
            name="notfound_hearing_events_uuid_route"
        )
        notfound_hearing_events_uuid_route.return_value = Response(404)

        exception_urn_uuid_route = respx_mock.get(
            "http://test-url/api/internal/v2/hearings/22d2222c-22ff-22ec-b222-2222ac222222/event_log/exception",
            name="exception_hearing_events_uuid_route")
        exception_urn_uuid_route.return_value = Response(500)

        # patch /laa_references
        pass_patch_maat = respx_mock.patch(
            "http://test-url/api/internal/v2/laa_references/22d2222c-22ff-22ec-b222-2222ac222222",
            name="laa_references_patch_pass_route")
        pass_patch_maat.return_value = Response(202)

        fail_patch_maat = respx_mock.patch(
            "http://test-url/api/internal/v2/laa_references/22d2222c-22ff-22ec-b222-2222ac222223",
            name="laa_references_patch_fail_route")
        fail_patch_maat.return_value = \
            Response(400, json={"error": "Contract failed with: {:maat_reference=>[\"3141592 has no common platform "
                                         "data created against Maat application.\"]}"})

        not_found_patch_maat = respx_mock.patch(
            "http://test-url/api/internal/v2/laa_references/22d2222c-22ff-22ec-b222-2222ac222224",
            name="laa_references_patch_not_found_route")
        not_found_patch_maat.return_value = Response(404)

        unprocessable_entity_patch_maat = respx_mock.patch(
            "http://test-url/api/internal/v2/laa_references/22d2222c-22ff-22ec-b222-2222ac222225",
            name="laa_references_patch_unprocessable_entity_route")
        unprocessable_entity_patch_maat.return_value = Response(422, json={"error": "Contract failed with: {"
                                                                                    ":maat_reference=>[\"3141592 has "
                                                                                    "no common platform data created "
                                                                                    "against Maat application.\"]}"})

        server_error_patch_maat = respx_mock.patch(
            "http://test-url/api/internal/v2/laa_references/22d2222c-22ff-22ec-b222-2222ac222226",
            name="laa_references_patch_server_error_route")
        server_error_patch_maat.return_value = Response(424)

        # post /laa_references

        pass_post_maat = respx_mock.post(
            "http://test-url/api/internal/v2/laa_references/",
            name="laa_references_post_pass_route",
            data=b'{"laa_reference": {"user_name": "pass-u", "defendant_id": null, "maat_reference": 1234567}}')
        pass_post_maat.return_value = Response(202)

        fail_post_maat = respx_mock.post(
            "http://test-url/api/internal/v2/laa_references/",
            name="laa_references_post_fail_route",
            json__laa_reference__user_name="fail-u")
        fail_post_maat.return_value = Response(400, json={"error": "Contract failed with: {:maat_reference=>[\"3141592 has no common platform data created against Maat application.\"]}"})

        not_found_post_maat = respx_mock.post(
            "http://test-url/api/internal/v2/laa_references/",
            name="laa_references_post_not_found_route",
            json__laa_reference__user_name="notfound-u")
        not_found_post_maat.return_value = Response(404)

        unprocessable_entity_post_maat = respx_mock.post(
            "http://test-url/api/internal/v2/laa_references/",
            name="laa_references_post_unprocessable_entity_route",
            json__laa_reference__user_name="unprocessable-u")
        unprocessable_entity_post_maat.return_value = Response(422, json={"error": "Contract failed with: {:maat_reference=>[\"3141592 has no common platform data created against Maat application.\"]}"})

        server_error_post_maat = respx_mock.post(
            "http://test-url/api/internal/v2/laa_references/",
            name="laa_references_post_server_error_route",
            json__laa_reference__user_name="servererror-u")
        server_error_post_maat.return_value = Response(424)

        yield respx_mock
