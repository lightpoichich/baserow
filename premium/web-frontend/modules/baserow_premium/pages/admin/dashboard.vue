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
              <div class="admin-dashboard__numbers-value">6336</div>
              <div class="admin-dashboard__numbers-percentage">
                <a href="#">view all</a>
              </div>
            </div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">Total groups</div>
              <div class="admin-dashboard__numbers-value">8762</div>
              <div class="admin-dashboard__numbers-percentage">
                <a href="#">view all</a>
              </div>
            </div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">
                Total applications
              </div>
              <div class="admin-dashboard__numbers-value">6336</div>
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
              <div class="admin-dashboard__numbers-value">8</div>
              <div class="admin-dashboard__numbers-percentage">
                <span class="admin-dashboard__numbers-percentage-value"
                  >+ 10.23%</span
                >
              </div>
            </div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">
                New users last 7 days
              </div>
              <div class="admin-dashboard__numbers-value">8</div>
              <div class="admin-dashboard__numbers-percentage">
                <span class="admin-dashboard__numbers-percentage-value"
                  >+ 10.23%</span
                >
              </div>
            </div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">
                New users last 24 hours
              </div>
              <div class="admin-dashboard__numbers-value">8</div>
              <div class="admin-dashboard__numbers-percentage">
                <span
                  class="admin-dashboard__numbers-percentage-value admin-dashboard__numbers-percentage-value--negative"
                  >- 10.23%</span
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
              <div class="admin-dashboard__numbers-value">8</div>
              <div class="admin-dashboard__numbers-percentage">
                <span class="admin-dashboard__numbers-percentage-value"
                  >+ 10.23%</span
                >
              </div>
            </div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">
                Active users last 7 days
              </div>
              <div class="admin-dashboard__numbers-value">8</div>
              <div class="admin-dashboard__numbers-percentage">
                <span class="admin-dashboard__numbers-percentage-value"
                  >+ 10.23%</span
                >
              </div>
            </div>
            <div class="admin-dashboard__numbers">
              <div class="admin-dashboard__numbers-name">
                Active users last 24 hours
              </div>
              <div class="admin-dashboard__numbers-value">8</div>
              <div class="admin-dashboard__numbers-percentage">
                <span
                  class="admin-dashboard__numbers-percentage-value admin-dashboard__numbers-percentage-value--negative"
                  >- 10.23%</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="admin-dashboard__box">
        <div class="admin-dashboard__box-dropdown">
          <Dropdown :value="'active_users_per_day'" :show-search="false">
            <DropdownItem
              name="Active users per day"
              value="active_users_per_day"
            ></DropdownItem>
            <DropdownItem
              name="New users per day"
              value="new_users_per_day"
            ></DropdownItem>
          </Dropdown>
        </div>
        <ActiveUsers></ActiveUsers>
      </div>
    </div>
  </div>
</template>

<script>
import ActiveUsers from '@baserow_premium/components/admin/dashboard/chars/ActiveUsers'

export default {
  components: { ActiveUsers },
  layout: 'app',
  middleware: 'staff',
}
</script>
