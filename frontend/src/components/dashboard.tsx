import ShinyText from "./ShinyText";
import StarBorder from "./StarBorder";
import { useEffect } from "react";

export default function Dashboard() {
  useEffect(() => {
    const bot = document.getElementById("polyrobot-container");
    const ask = document.getElementById("ask-query-btn");

    const hideBottom = () => {
      if (bot) bot.style.display = "none";
      if (ask) ask.style.display = "none";
    };
    const showBottom = () => {
      if (bot) bot.style.display = "";
      if (ask) ask.style.display = "";
    };

    const isChatOpen = (root: ShadowRoot) => {
      const iframe = root.querySelector("iframe") as HTMLIFrameElement | null;
      if (iframe) {
        try {
          const rect = iframe.getBoundingClientRect();
          const cs = window.getComputedStyle(iframe);
          if (
            rect.height > 10 &&
            cs.display !== "none" &&
            cs.visibility !== "hidden"
          )
            return true;
        } catch {}
      }

      const wrap = root.querySelector(
        ".df-messenger-wrapper"
      ) as HTMLElement | null;
      if (wrap) {
        const r = wrap.getBoundingClientRect();
        if (r.height > 120) return true;
        if (
          wrap.classList.contains("expanded") ||
          wrap.getAttribute("opened") === "true"
        )
          return true;
      }
      return false;
    };

    let observer: MutationObserver | null = null;
    const tryAttach = () => {
      const messenger = document.querySelector("df-messenger") as any | null;
      if (!messenger || !messenger.shadowRoot) return false;
      const root = messenger.shadowRoot as ShadowRoot;

      // Move widget circle to top-right
      const widgetIcon = root.querySelector("#widgetIcon") as HTMLElement | null;
      if (widgetIcon) {
        widgetIcon.style.position = "fixed";
        widgetIcon.style.top = "20px";
        widgetIcon.style.right = "20px";
        widgetIcon.style.bottom = "auto";
        widgetIcon.style.left = "auto";
        widgetIcon.style.zIndex = "9999";
      }


      // Initial sync — only apply hide/show on small screens
      if (window.innerWidth <= 768) {
        if (isChatOpen(root)) hideBottom();
        else showBottom();
      }

      const iconHandler = () => {
        setTimeout(() => {
          if (window.innerWidth <= 768) {
            if (isChatOpen(root)) hideBottom();
            else showBottom();
          } else {
            showBottom();
          }
        }, 150);
      };

      if (widgetIcon) {
        widgetIcon.addEventListener("click", iconHandler);
        (widgetIcon as any)._poly_iconHandler = iconHandler;
      }

      observer = new MutationObserver(() => {
        try {
          if (window.innerWidth <= 768) {
            if (isChatOpen(root)) hideBottom();
            else showBottom();
          } else {
            showBottom();
          }
        } catch {}
      });
      observer.observe(root, {
        subtree: true,
        childList: true,
        attributes: true,
      });

      messenger.style.zIndex = "10000";
      return true;
    };

    const starter = setInterval(() => {
      if (tryAttach()) clearInterval(starter);
    }, 300);

    return () => {
      clearInterval(starter);
      if (observer) observer.disconnect();
      try {
        const messenger = document.querySelector("df-messenger") as any | null;
        if (messenger && messenger.shadowRoot) {
          const root = messenger.shadowRoot as ShadowRoot;
          const widgetIcon = root.querySelector(
            "#widgetIcon"
          ) as HTMLElement | null;
          if (widgetIcon && (widgetIcon as any)._poly_iconHandler) {
            widgetIcon.removeEventListener(
              "click",
              (widgetIcon as any)._poly_iconHandler
            );
            delete (widgetIcon as any)._poly_iconHandler;
          }
        }
      } catch {}
    };
  }, []);

  const openChat = () => {
    const dfMessenger = document.querySelector("df-messenger") as any;
    if (dfMessenger && dfMessenger.shadowRoot) {
      const chatToggle = dfMessenger.shadowRoot.querySelector("#widgetIcon");
      if (chatToggle) {
        (chatToggle as HTMLElement).click();
        if (window.innerWidth <= 768) {
          const bot = document.getElementById("polyrobot-container");
          const ask = document.getElementById("ask-query-btn");
          if (bot) bot.style.display = "none";
          if (ask) ask.style.display = "none";
        }
      }
    }
  };

  return (
    <div className="h-screen overflow-hidden">
      <nav>
        <div className="text-4xl text-shadow-lg text-black fixed top-5 left-5 font-frederica">
          PolyGlot
        </div>

        <div
          className="fixed top-10 right-10"
          dangerouslySetInnerHTML={{
            __html: `
              <df-messenger
                intent="WELCOME"
                chat-title="Polyglot"
                agent-id="1c393f8d-f12d-49f3-8d7a-3945f8c80b83"
                language-code="en"
                chat-prompt="false"
              ></df-messenger>
            `,
          }}
        />
      </nav>

      <div className="w-full h-[450px] flex justify-center mt-10 xl:mt-0 items-center text-center">
        <div>
          <div className="justify-center items-center mb-5 text-5xl lg:text-6xl font-italiana">
            Ask Away Your <br />
            <span>
              <ShinyText
                text="Queries"
                disabled={false}
                speed={10}
                className="custom-class"
              />
            </span>
          </div>
          <div className="tracking-wider lg:text-lg text-gray-700">
            Ask anything about your institute - <br /> quick, simple, and
            reliable.
          </div>

          <div id="ask-query-btn" className="m-3">
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

      <div id="polyrobot-container" className="absolute -bottom-7 xl:-bottom-12 left-[50%] -translate-x-[50%]">
        <img
          src="/robot.gif"
          alt="Robot animation"
          className="w-[300px] mx-auto"
        />
      </div>
    </div>
  );
}
