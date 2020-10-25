import firebase from 'firebase/app'
import 'firebase/firestore'

// Get a Firestore instance
export const db = firebase
  .initializeApp({ projectId: 'bmwlog-app' })
  .firestore()

// Export types that exists in Firestore
// This is not always necessary
const { Timestamp, GeoPoint } = firebase.firestore
export { Timestamp, GeoPoint }
