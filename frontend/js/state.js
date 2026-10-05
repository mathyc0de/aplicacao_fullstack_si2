const AppState = {
  lastFilters: {},
  lastPayload: null,
};

function rememberSearch(filters, payload) {
  AppState.lastFilters = filters;
  AppState.lastPayload = payload;
}
