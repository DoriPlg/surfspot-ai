const initialState = {
    beaches:[]
}
export function beachReducer(state = initialState, action) {
    var newState = state
    switch (action.type) {
        case 'SET_BEACHES':
            newState = { ...state, beaches: action.beaches }
            break
        default:
    }
    return newState

}
