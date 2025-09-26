import React from "react";
import { cn } from "@/lib/utils";

const DoodleBackground = ({ children, className, opacity = 0.03 }) => {
  const doodleSvg = `
    <svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="doodle-pattern" x="0" y="0" width="400" height="400" patternUnits="userSpaceOnUse">
          <!-- Phone -->
          <rect x="80" y="20" width="40" height="60" rx="8" fill="none" stroke="white" stroke-width="2"/>
          <circle cx="100" cy="70" r="3" fill="none" stroke="white" stroke-width="1"/>
          <line x1="88" y1="30" x2="112" y2="30" stroke="white" stroke-width="1"/>
          <line x1="90" y1="35" x2="110" y2="35" stroke="white" stroke-width="1"/>
          <line x1="85" y1="40" x2="115" y2="40" stroke="white" stroke-width="1"/>
          
          <!-- Stars -->
          <path d="M40,50 L42,56 L48,56 L43,60 L45,66 L40,62 L35,66 L37,60 L32,56 L38,56 Z" fill="none" stroke="white" stroke-width="1.5"/>
          <path d="M160,80 L162,86 L168,86 L163,90 L165,96 L160,92 L155,96 L157,90 L152,86 L158,86 Z" fill="none" stroke="white" stroke-width="1.5"/>
          <path d="M320,40 L322,46 L328,46 L323,50 L325,56 L320,52 L315,56 L317,50 L312,46 L318,46 Z" fill="none" stroke="white" stroke-width="1.5"/>
          
          <!-- Hearts -->
          <path d="M200,30 C195,25 185,25 185,35 C185,25 175,25 170,30 C165,35 175,50 185,50 C195,50 205,35 200,30 Z" fill="none" stroke="white" stroke-width="1.5"/>
          <path d="M350,120 C347,117 342,117 342,122 C342,117 337,117 334,120 C331,123 337,130 342,130 C347,130 353,123 350,120 Z" fill="none" stroke="white" stroke-width="1.5"/>
          
          <!-- Smiley faces -->
          <circle cx="60" cy="150" r="20" fill="none" stroke="white" stroke-width="2"/>
          <circle cx="54" cy="145" r="2" fill="white"/>
          <circle cx="66" cy="145" r="2" fill="white"/>
          <path d="M52,158 Q60,165 68,158" fill="none" stroke="white" stroke-width="1.5"/>
          
          <circle cx="180" cy="200" r="18" fill="none" stroke="white" stroke-width="2"/>
          <circle cx="175" cy="195" r="1.5" fill="white"/>
          <circle cx="185" cy="195" r="1.5" fill="white"/>
          <path d="M172,208 Q180,214 188,208" fill="none" stroke="white" stroke-width="1.5"/>
          
          <!-- Speech bubbles -->
          <ellipse cx="280" cy="180" rx="25" ry="18" fill="none" stroke="white" stroke-width="2"/>
          <circle cx="273" cy="175" r="1" fill="white"/>
          <circle cx="280" cy="175" r="1" fill="white"/>
          <circle cx="287" cy="175" r="1" fill="white"/>
          <path d="M265,190 Q270,200 275,195" fill="none" stroke="white" stroke-width="2"/>
          
          <!-- Lightbulb -->
          <circle cx="340" cy="240" r="12" fill="none" stroke="white" stroke-width="2"/>
          <rect x="335" y="250" width="10" height="8" fill="none" stroke="white" stroke-width="1.5"/>
          <line x1="328" y1="230" x2="332" y2="234" stroke="white" stroke-width="1"/>
          <line x1="325" y1="240" x2="330" y2="240" stroke="white" stroke-width="1"/>
          <line x1="328" y1="250" x2="332" y2="246" stroke="white" stroke-width="1"/>
          <line x1="352" y1="230" x2="348" y2="234" stroke="white" stroke-width="1"/>
          <line x1="355" y1="240" x2="350" y2="240" stroke="white" stroke-width="1"/>
          <line x1="352" y1="250" x2="348" y2="246" stroke="white" stroke-width="1"/>
          
          <!-- Earth/Globe -->
          <circle cx="120" cy="300" r="22" fill="none" stroke="white" stroke-width="2"/>
          <path d="M100,300 Q110,290 120,300 Q130,310 140,300" fill="none" stroke="white" stroke-width="1.5"/>
          <path d="M105,315 Q115,305 125,315" fill="none" stroke="white" stroke-width="1.5"/>
          <ellipse cx="120" cy="300" rx="22" ry="8" fill="none" stroke="white" stroke-width="1"/>
          
          <!-- WiFi signals -->
          <path d="M240,120 Q250,110 260,120" fill="none" stroke="white" stroke-width="2"/>
          <path d="M243,123 Q250,118 257,123" fill="none" stroke="white" stroke-width="1.5"/>
          <path d="M246,126 Q250,123 254,126" fill="none" stroke="white" stroke-width="1"/>
          <circle cx="250" cy="128" r="1.5" fill="white"/>
          
          <!-- Email/Message -->
          <rect x="20" y="280" width="30" height="20" rx="2" fill="none" stroke="white" stroke-width="2"/>
          <path d="M20,280 L35,295 L50,280" fill="none" stroke="white" stroke-width="2"/>
          
          <!-- Charts/Graphs -->
          <rect x="280" y="320" width="4" height="15" fill="none" stroke="white" stroke-width="1.5"/>
          <rect x="286" y="315" width="4" height="20" fill="none" stroke="white" stroke-width="1.5"/>
          <rect x="292" y="310" width="4" height="25" fill="none" stroke="white" stroke-width="1.5"/>
          <rect x="298" y="305" width="4" height="30" fill="none" stroke="white" stroke-width="1.5"/>
          <rect x="304" y="312" width="4" height="23" fill="none" stroke="white" stroke-width="1.5"/>
          
          <!-- Cloud -->
          <ellipse cx="50" cy="200" rx="12" ry="8" fill="none" stroke="white" stroke-width="1.5"/>
          <ellipse cx="62" cy="200" rx="10" ry="6" fill="none" stroke="white" stroke-width="1.5"/>
          <ellipse cx="70" cy="195" rx="8" ry="5" fill="none" stroke="white" stroke-width="1.5"/>
          <ellipse cx="45" cy="195" rx="6" ry="4" fill="none" stroke="white" stroke-width="1.5"/>
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#doodle-pattern)"/>
    </svg>
  `;

  const backgroundStyle = {
    backgroundImage: `url("data:image/svg+xml,${encodeURIComponent(
      doodleSvg
    )}")`,
    backgroundSize: "300px 300px",
    backgroundRepeat: "repeat",
    backgroundPosition: "0 0",
    opacity: opacity,
  };

  return (
    <div className={cn("relative min-h-full flex-1", className)}>
      {/* Background overlay */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={backgroundStyle}
      />
      {/* Content */}
      <div className="z-10 min-h-full">{children}</div>
    </div>
  );
};

export default DoodleBackground;
