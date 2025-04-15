const express = require('express')
const { addReview } = require('./review.controller')
const router = express.Router()

// middleware that is specific to this router
// router.use(requireAuth)

// router.get('/', getReviews)
router.post('/',  addReview)
// router.get('/:id', getUser)
// router.put('/:id',  updateUser)
// router.get('/:id', getByName)rout
//  router.put('/:id',  updateUser)
// router.put('/:id', requireAuth,  updateUser)

// // router.put('/:id',  requireAuth, updateUser)
// router.delete('/:id',  requireAuth, requireAdmin, deleteUser)

module.exports = router