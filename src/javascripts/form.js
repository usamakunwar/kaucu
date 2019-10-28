$('select').selectpicker({
  noneResultsText: '',
});
setupSelectFieldData(['id_departure_airport', 'id_arrival_airport'], 'airports', ['iata', 'name'], 'iata');
setupSelectFieldData(['id_airline'], 'airlines', ['name'], 'name');
setupSelectFieldData(['id_hotel'], 'hotels');
setupSelectFieldData(['id_currency'], 'currencies');
setupSelectRemoteData(['id_user'], 'first_name', ['first_name','last_name']);
