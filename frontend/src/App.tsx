import { BrowserRouter, Route, Routes } from 'react-router-dom'

import Lessons from '@/pages/Lessons'
import Home from '@/pages/Home'

function App() {
  return (    
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/lessons" element={<Lessons />} />
        <Route path="/lessons/:id" element={<Lessons />} />
      </Routes>      
    </BrowserRouter>
  )
}

export default App
