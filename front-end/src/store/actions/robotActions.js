import { robotService } from '../../services/robotService'

export function loadRobots() {
  return async (dispatch, getState) => {
    const { filterBy } = getState().robotModule
    try {
      const robots = await robotService.query(filterBy)
      dispatch({ type: 'SET_ROBOTS', robots })
    } catch (err) {
      console.log(err);
    }
  }
}
export function getRobotById(robotId) {
  return async dispatch => {
    const robot = await robotService.getById(robotId)
    dispatch({ type: 'SET_ROBOT', robot })
  }
}
export function tryRobot(robotId) {
  return async dispatch => {
    const robot = await robotService.tryRobot(robotId)
    dispatch({ type: 'UPDATE_ROBOT', robot })
  }
}

export function removeRobot(robotId) {
  return async dispatch => {
    await robotService.remove(robotId)
    dispatch({ type: 'REMOVE_ROBOT', robotId })
  }
}

export function setFilterBy(filterBy) {
  return dispatch => {
    dispatch({ type: 'SET_FILTER_BY', filterBy })
  }
}
