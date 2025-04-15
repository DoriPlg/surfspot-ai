import React from 'react';
import {createRoot } from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom'
import { Provider } from 'react-redux'

import {store} from './store/store/store'
import {RootCmp} from './root-cmp';
import './assets/styles/styles.scss'

const rootElement = document.getElementById('root');
const root = createRoot(rootElement);


root.render(
<React.StrictMode>
    <Provider store={store}>
      <Router>
        <RootCmp />
      </Router>
    </Provider>
  </React.StrictMode>,
);