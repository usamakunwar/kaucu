$('select').selectpicker({
  noneResultsText: '',
});
$('#id_paid_date').datetimepicker();
setupSelectData(['id_departure_airport', 'id_arrival_airport'], 'airports', null, ['iata', 'name', 'city'], ['iata', 'name'], null, null );
setupSelectData(['id_airline'], 'airlines', null, ['name', 'iata'], ['name'], null, null );
setupSelectData(['id_hotel'], 'hotels', null, null, null, null, null );
setupSelectData(['id_currency'], 'currencies', null, null, null, null, null );
setupSelectData(['id_user'], null, '/contact/search/', null, ['first_name','last_name'], ['id'], ['slug']);