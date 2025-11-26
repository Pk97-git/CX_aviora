import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Settings as SettingsIcon } from "lucide-react"

export default function Settings() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <SettingsIcon className="h-5 w-5" />
            Configuration
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Configure integrations, user preferences, and system settings. This feature is coming soon.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
