import { storageService } from './storageService.js'
import { makeId } from './utilService.js'

export const robotService = {
    query,
    save,
    remove,
    getById,
    getEmptyRobot,
    tryRobot,
    getNextRobotId
}

const STORAGE_KEY = 'robots'

const gReviews = [
    {
        _id: 'abc101', createdAt: 1605855600000, swell:{appHeight: 0.8, avgHeight: 0.3,direction:285,period:7}, wind: { speed: 8, direction: 125 }, tide: { type: 'l', height: 0.13 }, beach: { _id: 'a101', name: 'sidny ali' },
        rate: 3, content: 'short and glassy waves', break: 'A',
    },
    { _id: 'r2', model: 'Dusty', batteryStatus: 100, type: 'Cleaning' },
    { _id: 'r3', model: 'Dominique Sote', batteryStatus: 100, type: 'Pleasure' },
    { _id: 'r4', model: 'DevTron', batteryStatus: 40, type: 'Office' }
]

var gRobots = _loadRobots()

function query(filterBy) {
    let robotsToReturn = gRobots;
    if (filterBy) {
        var { type, maxBatteryStatus, minBatteryStatus, model } = filterBy
        maxBatteryStatus = maxBatteryStatus || Infinity
        minBatteryStatus = minBatteryStatus || 0
        robotsToReturn = gRobots.filter(robot => robot.type.toLowerCase().includes(type.toLowerCase()) && robot.model.toLowerCase().includes(model.toLowerCase())
            && (robot.batteryStatus < maxBatteryStatus)
            && robot.batteryStatus > minBatteryStatus)
    }
    return Promise.resolve([...robotsToReturn]);
}

function tryRobot(id) {
    const robot = gRobots.find(robot => robot._id === id)
    robot.batteryStatus -= 10
    return Promise.resolve({ ...robot })
}

function getById(id) {
    const robot = gRobots.find(robot => robot._id === id)
    if (!robot) return Promise.reject()
    return Promise.resolve({ ...robot })
}

function remove(id) {
    const idx = gRobots.findIndex(robot => robot._id === id)
    gRobots.splice(idx, 1)
    if (!gRobots.length) gRobots = gDefaultRobots.slice()
    storageService.store(STORAGE_KEY, gRobots)
    return Promise.resolve()
}

function save(robotToSave) {
    if (robotToSave._id) {
        const idx = gRobots.findIndex(robot => robot._id === robotToSave._id)
        gRobots.splice(idx, 1, robotToSave)
    } else {
        robotToSave._id = makeId()
        gRobots.push(robotToSave)
    }
    storageService.store(STORAGE_KEY, gRobots)
    return Promise.resolve(robotToSave);
}

function getNextRobotId(robotId) {
    const robotIdx = gRobots.findIndex(robot => robot._id === robotId)
    let nextRobotIdx = robotIdx + 1
    if (nextRobotIdx === gRobots.length) nextRobotIdx = 0
    return gRobots[nextRobotIdx]._id
}

function getEmptyRobot() {
    return {
        model: '',
        type: '',
        batteryStatus: 100
    }
}

function _loadRobots() {
    let robots = storageService.load(STORAGE_KEY)
    if (!robots || !robots.length) robots = gDefaultRobots
    storageService.store(STORAGE_KEY, robots)
    return robots
}
32.18915644430349, 34.804633032007786
// https://api.stormglass.io/v2/weather/point?lat=32.18915644430349&lng=34.804633032007786&params=seaLevel,waveDirection,wavePeriod,time,swellHeight,currentDirection&key=8c27fa22-389a-11ec-b37c-0242ac130002-8c27fa90-389a-11ec-b37c-0242ac130002

https://api.stormglass.io/v2/tide/extremes/point?lat=32.18915644430349&lng=34.804633032007786&key=8c27fa22-389a-11ec-b37c-0242ac130002-8c27fa90-389a-11ec-b37c-0242ac130002