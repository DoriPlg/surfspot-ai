const beachService = require('./beach.service')
// const socketService = require('../../services/socket.service')
const logger = require('../../services/logger.service')


async function getBeaches(req, res) {
    try {
        const filterBy = {
            txt: req.query?.filterBy || '',
        }
        const beaches = await beachService.query(filterBy)
        res.send(beaches)
    } catch (err) {
        logger.error('Failed to get beaches', err)
        res.status(500).send({ err: 'Failed to get beaches' })
    }
}
async function addBeach(req, res) {
    try {
        const beach = req.body
        const savedBeach = await userService.add(beach)
        res.send(savedBeach)
    } catch (err) {
        logger.error('Failed to update user', err)
        res.status(500).send({ err: 'Failed to update user' })
    }
}
// async function getUser(req, res) {
//     try {
//         const user = await userService.getById(req.params.id)
       
//         res.send(user)
//     } catch (err) {
//         logger.error('Failed to get user', err)
//         res.status(500).send({ err: 'Failed to get user' })
//     }
// }


// async function deleteUser(req, res) {
//     try {
//         await userService.remove(req.params.id)
//         res.send({ msg: 'Deleted successfully' })
//     } catch (err) {
//         logger.error('Failed to delete user', err)
//         res.status(500).send({ err: 'Failed to delete user' })
//     }
// }

// async function updateUser(req, res) {
//     try {
//         const user = req.body
//         const savedUser = await userService.update(user)
//         res.send(savedUser)
//     } catch (err) {
//         logger.error('Failed to update user', err)
//         res.status(500).send({ err: 'Failed to update user' })
//     }
// }

module.exports = {
    getBeaches,
    addBeach
}