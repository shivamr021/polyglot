import ShinyText from "./ShinyText"
import StarBorder from './StarBorder'
import React, { useEffect } from "react";

export default function Dashboard() {
    useEffect(() => {
        const interval = setInterval(() => {
            const messenger = document.querySelector("df-messenger") as HTMLElement | null;
            if (messenger && messenger.shadowRoot) {
                const wrapper = messenger.shadowRoot.querySelector(".df-messenger-wrapper") as HTMLElement | null;
                if (wrapper) {
                    wrapper.style.position = "fixed"; // ensure fixed positioning
                    wrapper.style.bottom = "auto";    // reset bottom
                    wrapper.style.top = "70px";       // distance from top
                    wrapper.style.right = "20px";     // distance from right
                    clearInterval(interval);
                }
            }
        }, 500);

        return () => clearInterval(interval);
    }, []);

const openChat = () => {
    const dfMessenger = document.querySelector("df-messenger") as any;
    if (dfMessenger && dfMessenger.shadowRoot) {
      // the chat toggle button inside shadow DOM
      const chatToggle = dfMessenger.shadowRoot.querySelector("#widgetIcon");
      if (chatToggle) {
        (chatToggle as HTMLElement).click(); // simulate click to open
      }
    }
  };
    return (
        <>
            <div className="h-screen overflow-hidden">
                <nav>
                    <div className='text-4xl text-shadow-lg text-black fixed top-5 left-5 font-frederica'>PolyGlot</div>
                    <div className="fixed top-5 right-5 border rounded-full p-3 cursor-pointer">bot
                        <div className="fixed top-10 right-10" dangerouslySetInnerHTML={{
                            __html: `
                                <df-messenger
                                intent="WELCOME"
                                chat-title="Polyglot"
                                agent-id="1c393f8d-f12d-49f3-8d7a-3945f8c80b83"
                                language-code="en"
                                ></df-messenger>
                            ` }} />
                    </div>
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
                        <div className='tracking-wider lg:text-lg m-5 text-gray-700 '>Ask anything about your institute - <br /> quick, simple, and reliable.</div>
                        {/* <button className='p-5 px-20 rounded-full ring-2 text-white hover:shadow-xl shadow-gray-400 active:bg-gray-800 ring-white font-bold bg-black'>Search</button> */}
                        <div className="">
                            <StarBorder
                                as="button"
                                onClick={openChat}
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