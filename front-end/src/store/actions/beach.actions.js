import {beachService} from "../../services/beach.service.js";

export function loadBeaches() {
    return async (dispatch) => {
        try {
            let beaches = await beachService.query()
            console.log(beaches);
            dispatch({
                type: 'SET_BEACHES',
                beaches
            })
        }
        catch (err) {
            console.log(`Had Issues ${err}`)
            throw err
        }
    }
}
