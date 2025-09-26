import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { cn } from "@/lib/utils";
import { Droplets, Wind, Eye, Gauge, Clock } from "lucide-react";

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

  // Determine weather theme class
  const getWeatherTheme = (emoji) => {
    if (emoji.includes("☀️")) {
      return "weather-sunny";
    }
    if (emoji.includes("🌧️") || emoji.includes("🌦️")) {
      return "weather-rainy";
    }
    if (emoji.includes("❄️")) {
      return "weather-snowy";
    }
    if (emoji.includes("⛈️")) {
      return "weather-stormy";
    }
    if (emoji.includes("☁️")) {
      return "weather-cloudy";
    }
    return "bg-gradient-to-br from-blue-400 to-blue-600";
  };

  const WeatherMetric = ({ icon, label, value, unit = "" }) => (
    <div className="flex items-center gap-2 text-sm">
      <div className="text-white/80">{icon}</div>
      <div className="flex-1">
        <div className="text-white/70 text-xs">{label}</div>
        <div className="text-white font-medium">
          {value}
          {unit}
        </div>
      </div>
    </div>
  );

  return (
    <div className={cn("w-full max-w-md", className)}>
      {/* Current Weather Card */}
      <Card
        className={cn(
          "overflow-hidden border-0 text-white",
          getWeatherTheme(weatherData.current.emoji || "🌤️")
        )}
      >
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-3 text-white">
            <span className="text-3xl">{weatherData.current.emoji}</span>
            <div>
              <div className="text-lg font-medium">{weatherData.location}</div>
              <div className="text-white/80 text-sm font-normal">
                {weatherData.current.description}
              </div>
            </div>
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Temperature */}
          {weatherData.current.temperature && (
            <div className="text-center">
              <div className="text-4xl font-bold text-white">
                {weatherData.current.temperature}°C
              </div>
              {weatherData.current.feelsLike && (
                <div className="text-white/70 text-sm">
                  {isJapanese ? "体感" : "Feels like"}{" "}
                  {weatherData.current.feelsLike}°C
                </div>
              )}
            </div>
          )}

          {/* Weather Metrics Grid */}
          <div className="grid grid-cols-2 gap-4">
            {weatherData.current.humidity && (
              <WeatherMetric
                icon={<Droplets className="w-4 h-4" />}
                label={isJapanese ? "湿度" : "Humidity"}
                value={weatherData.current.humidity}
                unit="%"
              />
            )}

            {weatherData.current.windSpeed && (
              <WeatherMetric
                icon={<Wind className="w-4 h-4" />}
                label={isJapanese ? "風速" : "Wind"}
                value={weatherData.current.windSpeed}
                unit=" m/s"
              />
            )}

            {weatherData.current.pressure && (
              <WeatherMetric
                icon={<Gauge className="w-4 h-4" />}
                label={isJapanese ? "気圧" : "Pressure"}
                value={weatherData.current.pressure}
                unit=" hPa"
              />
            )}

            {weatherData.current.visibility && (
              <WeatherMetric
                icon={<Eye className="w-4 h-4" />}
                label={isJapanese ? "視界" : "Visibility"}
                value={weatherData.current.visibility}
                unit=" km"
              />
            )}
          </div>
        </CardContent>
      </Card>

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

      {/* Fallback: Display original content if parsing fails */}
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
