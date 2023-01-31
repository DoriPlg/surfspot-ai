const express = require('express')
const { getBeaches, addBeach } = require('./beach.controller')
const router = express.Router()

// middleware that is specific to this router
// router.use(requireAuth)

router.get('/', getBeaches)
router.post('/',  addBeach)
// router.get('/:id', getUser)
// router.put('/:id',  updateUser)
// router.get('/:id', getByName)rout
//  router.put('/:id',  updateUser)
// router.put('/:id', requireAuth,  updateUser)

// // router.put('/:id',  requireAuth, updateUser)
// router.delete('/:id',  requireAuth, requireAdmin, deleteUser)

module.exports = router