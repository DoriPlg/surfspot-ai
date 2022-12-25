const express = require('express')
const { requireAuth, requireAdmin } = require('../../middlewares/requireAuth.middleware')
const { getUser, getUsers, deleteUser, updateUser, addBeach } = require('./user.controller')
const router = express.Router()

// middleware that is specific to this router
// router.use(requireAuth)

router.get('/', getUsers)
router.post('/',  addBeach)
router.get('/:id', getUser)
router.put('/:id',  updateUser)
// router.get('/:id', getByName)rout
//  router.put('/:id',  updateUser)
// router.put('/:id', requireAuth,  updateUser)

// // router.put('/:id',  requireAuth, updateUser)
// router.delete('/:id',  requireAuth, requireAdmin, deleteUser)

module.exports = router