<template>
  <div class="layout__col-2-scroll">
    <div class="admin-dashboard">
      <h1>Dashboard</h1>
      <div class="row margin-bottom-3">
        <div class="col col-4">
          <div class="admin-dashboard__box">
            <div class="admin-dashboard__box-title">Totals</div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">Total users</div>
              <div class="admin-dashboard__numbers-value">
                {{ total_users }}
              </div>
              <div class="admin-dashboard__numbers-percentage">
                <nuxt-link :to="{ name: 'admin-users' }">view all</nuxt-link>
              </div>
            </div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">Total groups</div>
              <div class="admin-dashboard__numbers-value">
                {{ total_groups }}
              </div>
              <div class="admin-dashboard__numbers-percentage"></div>
            </div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">
                Total applications
              </div>
              <div class="admin-dashboard__numbers-value">
                {{ total_applications }}
              </div>
            </div>
          </div>
        </div>
        <div class="col col-4">
          <div class="admin-dashboard__box">
            <div class="admin-dashboard__box-title">New users</div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">
                New users last 24 hours
              </div>
              <div class="admin-dashboard__numbers-value">
                {{ new_users_last_24_hours }}
              </div>
              <div class="admin-dashboard__numbers-percentage">
                <span
                  class="admin-dashboard__numbers-percentage-value"
                  :class="{
                    'admin-dashboard__numbers-percentage-value--negative': isNegative(
                      percentages.new_users_last_24_hours
                    ),
                  }"
                  >{{ percentages.new_users_last_24_hours }}</span
                >
              </div>
            </div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">
                New users last 7 days
              </div>
              <div class="admin-dashboard__numbers-value">
                {{ new_users_last_7_days }}
              </div>
              <div class="admin-dashboard__numbers-percentage">
                <span
                  class="admin-dashboard__numbers-percentage-value"
                  :class="{
                    'admin-dashboard__numbers-percentage-value--negative': isNegative(
                      percentages.new_users_last_7_days
                    ),
                  }"
                  >{{ percentages.new_users_last_7_days }}</span
                >
              </div>
            </div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">
                New users last 30 days
              </div>
              <div class="admin-dashboard__numbers-value">
                {{ new_users_last_30_days }}
              </div>
              <div class="admin-dashboard__numbers-percentage">
                <span
                  class="admin-dashboard__numbers-percentage-value"
                  :class="{
                    'admin-dashboard__numbers-percentage-value--negative': isNegative(
                      percentages.new_users_last_30_days
                    ),
                  }"
                  >{{ percentages.new_users_last_30_days }}</span
                >
              </div>
            </div>
          </div>
        </div>
        <div class="col col-4">
          <div class="admin-dashboard__box">
            <div class="admin-dashboard__box-title">Active users</div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">
                Active users last 24 hours
              </div>
              <div class="admin-dashboard__numbers-value">
                {{ active_users_last_24_hours }}
              </div>
              <div class="admin-dashboard__numbers-percentage">
                <span
                  class="admin-dashboard__numbers-percentage-value"
                  :class="{
                    'admin-dashboard__numbers-percentage-value--negative': isNegative(
                      percentages.new_users_last_30_days
                    ),
                  }"
                  >{{ percentages.active_users_last_24_hours }}</span
                >
              </div>
            </div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">
                Active users last 7 days
              </div>
              <div class="admin-dashboard__numbers-value">
                {{ active_users_last_7_days }}
              </div>
              <div class="admin-dashboard__numbers-percentage">
                <span
                  class="admin-dashboard__numbers-percentage-value"
                  :class="{
                    'admin-dashboard__numbers-percentage-value--negative': isNegative(
                      percentages.active_users_last_7_days
                    ),
                  }"
                  >{{ percentages.active_users_last_7_days }}</span
                >
              </div>
            </div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">
                Active users last 30 days
              </div>
              <div class="admin-dashboard__numbers-value">
                {{ active_users_last_30_days }}
              </div>
              <div class="admin-dashboard__numbers-percentage">
                <span
                  class="admin-dashboard__numbers-percentage-value"
                  :class="{
                    'admin-dashboard__numbers-percentage-value--negative': isNegative(
                      percentages.active_users_last_30_days
                    ),
                  }"
                  >{{ percentages.active_users_last_30_days }}</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="admin-dashboard__box">
        <ActiveUsers
          :new-users="new_users_per_day"
          :active-users="active_users_per_day"
        ></ActiveUsers>
      </div>
    </div>
  </div>
</template>

<script>
import ActiveUsers from '@baserow_premium/components/admin/dashboard/chars/ActiveUsers'
import AdminDashboardService from '@baserow_premium/services/adminDashboard'

export default {
  components: { ActiveUsers },
  layout: 'app',
  middleware: 'staff',
  async asyncData({ app }) {
    const { data } = await AdminDashboardService(app.$client).dashboard()
    return data
  },
  computed: {
    percentages() {
      const percentage = (value1, value2) => {
        if (value1 === 0 || value2 === 0) {
          return ''
        }

        let value = value1 / value2 - 1
        value = Math.round(value * 100 * 100) / 100
        value = `${value > 0 ? '+ ' : '- '}${Math.abs(value)}%`
        return value
      }
      return {
        new_users_last_24_hours: percentage(
          this.new_users_last_24_hours,
          this.previous_new_users_last_24_hours
        ),
        new_users_last_7_days: percentage(
          this.new_users_last_7_days,
          this.previous_new_users_last_7_days
        ),
        new_users_last_30_days: percentage(
          this.new_users_last_30_days,
          this.previous_new_users_last_30_days
        ),
        active_users_last_24_hours: percentage(
          this.active_users_last_24_hours,
          this.previous_active_users_last_24_hours
        ),
        active_users_last_7_days: percentage(
          this.active_users_last_7_days,
          this.previous_active_users_last_7_days
        ),
        active_users_last_30_days: percentage(
          this.active_users_last_30_days,
          this.previous_active_users_last_30_days
        ),
      }
    },
  },
  methods: {
    isNegative(value) {
      return value.substr(0, 1) === '-'
    },
  },
}
</script>
