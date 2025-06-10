import pytest
from src.models.report_model import Report

@pytest.fixture
def sample_report(client):
    # Crear un reporte de prueba en DB antes de tests de respuestas
    r = Report(user_id='test_user', description='Reporte test')
    r.save()
    return str(r.id)


def test_create_response_success(client, sample_report):
    headers = {'X-User-Id': 'test_user'}  # usando DEV_MODE
    payload = {
        'type': 'avistamiento',
        'comment': 'Lo vi cerca de mi casa',
        'location': {
            'type': 'Point',
            'coordinates': [-74.03, 4.67]
        }
    }
    res = client.post(f'/responses/{sample_report}', json=payload, headers=headers)
    assert res.status_code == 201
    data = res.get_json()
    assert data['report_id'] == sample_report
    assert data['type'] == 'avistamiento'
    assert data['resp_user_id'] == 'test_user'


def test_create_response_closed_report(client, sample_report):
    # Cerrar reporte manualmente
    from src.models.report_model import Report
    rpt = Report.objects.get(id=sample_report)
    rpt.status = 'closed'; rpt.save()

    headers = {'X-User-Id': 'test_user'}
    payload = {'type': 'avistamiento', 'comment': 'Prueba', 'location': {'type': 'Point', 'coordinates': [0,0]}}
    res = client.post(f'/reports/{sample_report}/responses', json=payload, headers=headers)
    assert res.status_code == 403
    assert res.get_json()['message'] == 'No se pueden agregar respuestas a un reporte cerrado'