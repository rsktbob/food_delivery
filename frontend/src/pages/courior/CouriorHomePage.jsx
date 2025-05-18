import CouriorOrderList from '../../components/CourierOrderList';

function CouriorHomePage({user}){
  // Sample order data Restaurant, distance, fee
  return(
    <CouriorOrderList user={user}/>
  )
}

export default CouriorHomePage