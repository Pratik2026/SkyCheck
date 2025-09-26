import React from "react";
import robot from "../../assets/robot.gif";

const Welcome = ({ language = "english" }) => {
  const t =
    language === "japanese"
      ? {
          title: "SkyCheck - 天気インテリジェンス・チャットボット",
          subtitle: "ようこそ！質問があれば、何でも聞いてください。",
        }
      : {
          title: "SkyCheck - A Weather Intelligence Based Chatbot",
          subtitle: "Welcome! Have a question? Ask me!",
        };

  return (
    <div className="relative h-full w-full overflow-hidden font-sans">
      {/* Soft spotlight behind the bot */}
      <div
        className="pointer-events-none absolute inset-0
                   [background:radial-gradient(60%_40%_at_50%_30%,rgba(80,100,140,.2),transparent_60%)]"
      />

      {/* Dimmed background pattern pass-through (optional) */}
      <div className="pointer-events-none absolute inset-0 opacity-[0.06]" />

      {/* Content */}
      <div className="relative h-full flex items-center justify-center">
        <div className="text-center px-6 max-w-5xl animate-in fade-in duration-500">
          {/* Bot */}
          <img
            src={robot}
            alt="Robot"
            className="mx-auto w-40 h-40 md:w-48 md:h-48 select-none
                       drop-shadow-[0_8px_24px_rgba(0,0,0,0.35)]
                       motion-safe:animate-[float_5s_ease-in-out_infinite]"
            draggable={false}
          />

          {/* Title — indigo/blue gradient to match theme */}
          <h1
            className="mt-6 text-3xl md:text-4xl font-extrabold tracking-tight leading-tight
                       font-[Inter]
                       bg-gradient-to-r
                       from-indigo-200 via-indigo-300 to-blue-300
                       dark:from-gray-300 dark:via-gray-400 dark:to-gray-300
                       bg-clip-text text-transparent
                       drop-shadow-[0_2px_20px_rgba(80,120,200,0.15)]"
          >
            {t.title}
          </h1>

          {/* Subtitle */}
          <p className="mt-3 text-base md:text-lg text-muted-foreground font-[Inter]">
            {t.subtitle}
          </p>
        </div>
      </div>

      {/* keyframes for subtle float */}
      <style>{`
        @keyframes float {
          0%   { transform: translateY(0px); }
          50%  { transform: translateY(-6px); }
          100% { transform: translateY(0px); }
        }
      `}</style>
    </div>
  );
};

export default Welcome;
