import { BrowserRouter, Route, Routes } from 'react-router-dom'

import Home from '@/pages/Home'
import Lessons from '@/pages/Lessons'
import Study from '@/pages/Study'
import Results  from '@/pages/Results'

function App() {
  return (    
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/lessons" element={<Lessons />} />
        <Route path="/lessons/:id" element={<Study />} />
        <Route path="/results" element={<Results />} />
      </Routes>      
    </BrowserRouter>
  )
}

export default App
