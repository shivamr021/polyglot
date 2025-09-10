import ShinyText from "./ShinyText"
import StarBorder from './StarBorder'

export default function Dashboard() {
    return (
        <>
            <div className="h-screen overflow-hidden">
                <nav>
                    <div className='text-2xl text-shadow-lg text-[#3b1a6f] font-mono fixed top-5 left-5 font-fascinate font-bold'>PolyGlot</div>
                    <div className="fixed top-5 right-5 border rounded-full p-3 cursor-pointer">bot</div>
                </nav>
                <div className='w-full h-[500px] flex justify-center items-center text-center'>
                    <div>
                        <div className='justify-center items-center text-5xl lg:text-6xl font-italiana'>Ask Away Your <br />
                        <span className="">
                            <ShinyText
                                text="Queries"
                                disabled={false}
                                speed={10}
                                className='custom-class'
                            />
                            </span>
                        </div>
                        <div className='tracking-wider lg:text-lg m-5  text-gray-700'>Ask anything about your institute - <br /> quick, simple, and reliable.</div>
                        {/* <button className='p-5 px-20 rounded-full ring-2 text-white hover:shadow-xl shadow-gray-400 active:bg-gray-800 ring-white font-bold bg-black'>Search</button> */}
                        <div className="">
                            <StarBorder
                                as="button"
                                className="custom-class"
                                color="#7C00FE"
                                thickness={6}
                                speed="5s"
                            >
                                Ask query
                            </StarBorder>
                        </div>
                    </div>
                </div>
                <div className="">
                    <img
                        src="/robot.gif"
                        alt="Robot animation"
                        className="w-full max-w-[300px] mx-auto"
                    />
                </div>
            </div>
        </>
    )
}