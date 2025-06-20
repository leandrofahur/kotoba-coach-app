import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

function Home() {
    const navigate = useNavigate();

    const handleStart = () => {
        navigate("/lessons");
    }

    return (
        <div className="flex flex-col items-center justify-center h-screen bg-beige-light p-4 gap-4">
            <Button className="text-xl font-bold" onClick={handleStart}>START</Button>
        </div>
    )
}

export default Home;