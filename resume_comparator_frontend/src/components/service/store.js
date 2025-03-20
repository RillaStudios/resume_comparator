// Code for creating the Redux store
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';


/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250320
 Description: This function sets up the Redux store
*/
const store = configureStore({
  reducer: {
    auth: authReducer,
  },
  devTools: true,
});

export default store;