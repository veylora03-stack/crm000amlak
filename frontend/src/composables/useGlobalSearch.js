import { ref, computed } from 'vue'
import { useClientsStore } from '@/stores/clients'
import { usePropertiesStore } from '@/stores/properties'
import { useDealsStore } from '@/stores/deals'
import { useTasksStore } from '@/stores/tasks'

export function useGlobalSearch() {
  const clientsStore = useClientsStore()
  const propertiesStore = usePropertiesStore()
  const dealsStore = useDealsStore()
  const tasksStore = useTasksStore()

  const query = ref('')
  const loading = ref(false)
  const hasSearched = ref(false)

  const clientResults = computed(() => {
    if (!query.value.trim()) {
      return []
    }

    const q = query.value.trim().toLowerCase()

    return clientsStore.items
      .filter((client) => {
        return (
          client.full_name.toLowerCase().includes(q) ||
          client.phone.toLowerCase().includes(q) ||
          (client.email && client.email.toLowerCase().includes(q))
        )
      })
      .slice(0, 5)
  })

  const propertyResults = computed(() => {
    if (!query.value.trim()) {
      return []
    }

    const q = query.value.trim().toLowerCase()

    return propertiesStore.items
      .filter((property) => {
        return (
          property.title.toLowerCase().includes(q) ||
          property.code.toLowerCase().includes(q) ||
          property.address.toLowerCase().includes(q) ||
          property.city.toLowerCase().includes(q)
        )
      })
      .slice(0, 5)
  })

  const dealResults = computed(() => {
    if (!query.value.trim()) {
      return []
    }

    const q = query.value.trim().toLowerCase()

    return dealsStore.deals
      .filter((deal) => {
        return (
          deal.title.toLowerCase().includes(q) ||
          (deal.client_name && deal.client_name.toLowerCase().includes(q)) ||
          (deal.property_title && deal.property_title.toLowerCase().includes(q))
        )
      })
      .slice(0, 5)
  })

  const taskResults = computed(() => {
    if (!query.value.trim()) {
      return []
    }

    const q = query.value.trim().toLowerCase()

    return tasksStore.items
      .filter((task) => {
        return (
          task.title.toLowerCase().includes(q) ||
          (task.description && task.description.toLowerCase().includes(q)) ||
          (task.assigned_user && task.assigned_user.toLowerCase().includes(q))
        )
      })
      .slice(0, 5)
  })

  const totalResults = computed(() => {
    return (
      clientResults.value.length +
      propertyResults.value.length +
      dealResults.value.length +
      taskResults.value.length
    )
  })

  const hasResults = computed(() => {
    return totalResults.value > 0
  })

  async function search(searchQuery) {
    query.value = searchQuery

    if (!searchQuery.trim()) {
      hasSearched.value = false
      loading.value = false
      return
    }

    loading.value = true
    hasSearched.value = true

    await Promise.all([
      clientsStore.fetchClients(),
      propertiesStore.fetchProperties(),
      dealsStore.fetchDeals(),
      tasksStore.fetchTasks()
    ])

    loading.value = false
  }

  function clearSearch() {
    query.value = ''
    hasSearched.value = false
    loading.value = false
  }

  return {
    query,
    loading,
    hasSearched,
    clientResults,
    propertyResults,
    dealResults,
    taskResults,
    totalResults,
    hasResults,
    search,
    clearSearch
  }
}
