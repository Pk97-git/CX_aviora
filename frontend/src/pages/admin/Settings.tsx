import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useToast } from '@/hooks/use-toast'
import { adminApi, Tenant } from '@/lib/api/admin'
import { Save } from 'lucide-react'

export default function AdminSettingsPage() {
  const [tenant, setTenant] = useState<Tenant | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const { toast } = useToast()

  const [name, setName] = useState('')

  useEffect(() => {
    loadTenant()
  }, [])

  const loadTenant = async () => {
    try {
      const data = await adminApi.getTenant()
      setTenant(data)
      setName(data.name)
    } catch (error: any) {
      toast({
        title: 'Error',
        description: 'Failed to load tenant information',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      await adminApi.updateTenant({ name })
      toast({
        title: 'Success',
        description: 'Settings updated successfully',
      })
      loadTenant()
    } catch (error: any) {
      toast({
        title: 'Error',
        description: error.response?.data?.detail || 'Failed to update settings',
        variant: 'destructive',
      })
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto py-6 max-w-4xl">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Organization Settings</h1>
        <p className="text-muted-foreground">Manage your organization's configuration</p>
      </div>

      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>General Information</CardTitle>
            <CardDescription>Basic organization details</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Organization Name</Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Acme Inc"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="slug">Organization Slug</Label>
              <Input
                id="slug"
                value={tenant?.slug || ''}
                disabled
                className="bg-muted"
              />
              <p className="text-xs text-muted-foreground">
                Slug cannot be changed after creation
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="plan">Current Plan</Label>
              <Input
                id="plan"
                value={tenant?.plan || ''}
                disabled
                className="bg-muted capitalize"
              />
            </div>
            <Button onClick={handleSave} disabled={saving}>
              <Save className="mr-2 h-4 w-4" />
              {saving ? 'Saving...' : 'Save Changes'}
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Organization ID</CardTitle>
            <CardDescription>Use this ID for API integrations</CardDescription>
          </CardHeader>
          <CardContent>
            <code className="block p-3 bg-muted rounded-md text-sm">
              {tenant?.id}
            </code>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
