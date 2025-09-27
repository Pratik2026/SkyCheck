import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { cn } from "@/lib/utils";
import { Droplets, Wind, Eye, Gauge } from "lucide-react";

const WeatherDisplay = ({ content, language, className }) => {
  // Parse weather information from the formatted content
  const parseWeatherData = (text) => {
    const lines = text.split("\n").filter((line) => line.trim());
    const weatherData = {
      location: "",
      current: {},
      forecast: [],
    };

    let currentSection = "header";

    lines.forEach((line) => {
      line = line.trim();

      // Location header
      if (line.includes("🌍")) {
        const locationMatch = line.match(/🌍\s+(.+)/);
        if (locationMatch) {
          weatherData.location = locationMatch[1]
            .replace("Weather for ", "")
            .replace("の天気情報", "");
        }
      }

      // Current weather data
      if (line.includes("🌡️")) {
        const tempMatch = line.match(/🌡️\s+(.+?)(\d+)°C.*?(\d+)°C/);
        if (tempMatch) {
          weatherData.current.temperature = parseInt(tempMatch[2]);
          weatherData.current.feelsLike = parseInt(tempMatch[3]);
        }
      }

      if (line.includes("💧")) {
        const humidityMatch = line.match(/💧\s+.*?(\d+)%/);
        if (humidityMatch) {
          weatherData.current.humidity = parseInt(humidityMatch[1]);
        }
      }

      if (line.includes("🌀")) {
        const pressureMatch = line.match(/🌀\s+.*?(\d+)\s+hPa/);
        if (pressureMatch) {
          weatherData.current.pressure = parseInt(pressureMatch[1]);
        }
      }

      if (line.includes("💨")) {
        const windMatch = line.match(/💨\s+.*?([\d.]+)\s+m\/s/);
        if (windMatch) {
          weatherData.current.windSpeed = parseFloat(windMatch[1]);
        }
      }

      if (line.includes("👁️")) {
        const visibilityMatch = line.match(/👁️\s+.*?([\d.]+)\s+km/);
        if (visibilityMatch) {
          weatherData.current.visibility = parseFloat(visibilityMatch[1]);
        }
      }

      // Current weather description
      // eslint-disable-next-line no-misleading-character-class
      if (line.match(/^[⛈️🌦️🌧️❄️🌫️☀️☁️🌤️]/u)) {
        const parts = line.split(":");
        if (parts.length > 1) {
          weatherData.current.emoji = parts[0].trim();
          weatherData.current.description = parts[1].trim();
        }
      }

      // Forecast section
      if (line.includes("📅")) {
        currentSection = "forecast";
      } else if (
        currentSection === "forecast" &&
        // eslint-disable-next-line no-misleading-character-class
        line.match(/^[⛈️🌦️🌧️❄️🌫️☀️☁️🌤️]/u)
      ) {
        const forecastMatch = line.match(
          // eslint-disable-next-line no-misleading-character-class
          /^([⛈️🌦️🌧️❄️🌫️☀️☁️🌤️])\s+(.+?):\s+(\d+)°C\s+\/\s+(\d+)°C\s+-\s+(.+)/u
        );
        if (forecastMatch) {
          weatherData.forecast.push({
            emoji: forecastMatch[1],
            date: forecastMatch[2],
            tempMax: parseInt(forecastMatch[3]),
            tempMin: parseInt(forecastMatch[4]),
            description: forecastMatch[5],
          });
        }
      }
    });

    return weatherData;
  };

  const weatherData = parseWeatherData(content);
  const isJapanese = language === "japanese";

  return (
    <div className={cn("w-full max-w-md", className)}>

      {/* Forecast Cards */}
      {weatherData.forecast.length > 0 && (
        <div className="mt-4 space-y-2">
          <h4 className="text-sm font-medium text-muted-foreground px-1">
            {isJapanese ? "3日間の予報" : "3-Day Forecast"}
          </h4>
          <div className="space-y-2">
            {weatherData.forecast.map((day, index) => (
              <Card key={index} className="bg-muted/50">
                <CardContent className="flex items-center gap-3 p-3">
                  <span className="text-xl">{day.emoji}</span>
                  <div className="flex-1">
                    <div className="text-sm font-medium">{day.date}</div>
                    <div className="text-xs text-muted-foreground">
                      {day.description}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-medium">
                      {day.tempMax}° / {day.tempMin}°
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {!weatherData.location && (
        <Card>
          <CardContent className="p-4">
            <div
              className={cn(
                "whitespace-pre-wrap text-sm",
                language === "japanese" && "japanese-text"
              )}
            >
              {content}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default WeatherDisplay;
