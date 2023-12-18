import './index.css'
import { useState, useEffect } from 'react'


function App(){
  const [productName, setproductName] = useState(null);
  const [responseList, setresponseList] = useState([]);

  async function getResult(){
    setresponseList(['processing...'])
    try {
      fetch('http://localhost:4000', {
        method: 'POST',
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({'product_name' : productName})
      })
      .then((response) => response.json())
      .then((result) => setresponseList(Object.values(result)))
    } catch (error) {
      console.log(error);
      setresponseList(["failed to get result, try again with better naming for the product"])
    }
  }

  function test(){
    console.log(productName);
    setresponseList(['one','two','three','four'])
  }

  return (
    <>
    <h2>amazon vs flipkart price comparator</h2>
    <div className='mainContainer'>
    <div className='inputContainer'>
    <input type="text" onChange={(event) => setproductName(event.target.value)}/>
    <button onClick={() => getResult()}>compare</button>
    </div>
    <div className='compareBar'>
      <div className='resultContainer'>{responseList.length === 0 ? <div>Search a product now...</div> : responseList.map((item, index) => (
        <div className='resultbar' key={index}>{item}</div>
      ))}</div>
    </div>
    </div>
    </>
  )
}

export default App;