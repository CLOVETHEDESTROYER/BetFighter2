function parseWinnerData(data) {
  // Parse the JSON string and extract the required fields
  // Replace "player1Won" and "player2Won" with the correct keys from the JSON data
  const parsedData = JSON.parse(data);
  const _player1Won = parsedData.player1Won;
  const _player2Won = parsedData.player2Won;

  return { _player1Won, _player2Won };
}