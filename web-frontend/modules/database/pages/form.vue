<template>
  <div class="form-view__page">
    <div
      class="form-view__cover"
      style="
        background-image: url('https://pixabay.com/get/g4015878569ca8dda5c97206e6ea31123a82bb90ec32e32408e40dc73ca7bb9d4c34fb5fd4b12624b2bfb2a4d0f636a72_1920.jpg');
      "
    ></div>
    <div class="form-view__body">
      <div class="form-view__heading">
        <div class="form_view__logo">
          <img
            class="form_view__logo-img"
            src="@baserow/modules/core/static/img/logo.svg"
            width="200"
          />
        </div>
        <h1 class="form-view__title">Custom title</h1>
        <p class="form-view__description">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi
          gravida, tellus vel finibus blandit, urna ligula egestas nisi, in
          hendrerit nibh purus porta velit. Praesent id
        </p>
      </div>
      <div class="form-view__field">
        <div class="form-view__field-inner">
          <div class="form-view__field-name">Custom name</div>
          <div class="form-view__field-description">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi
            gravida, tellus vel.
          </div>
          <div class="form-view__field-control">
            <input type="text" name="" value="" class="input input--large" />
          </div>
        </div>
      </div>
      <div class="form-view__field">
        <div class="form-view__field-inner">
          <div class="form-view__field-name">Custom name</div>
          <div class="form-view__field-description">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi
            gravida, tellus vel.
          </div>
          <div class="form-view__field-control">
            <input type="text" name="" value="" class="input input--large" />
          </div>
        </div>
      </div>
      <div class="form-view__actions">
        <div class="form-view__powered-by">
          Powered by
          <a href="https://baserow.io" target="_blank">
            <img
              class="form-view__powered-by-logo"
              src="@baserow/modules/core/static/img/logo.svg"
              alt=""
            />
          </a>
        </div>
        <div class="form-view__submit">
          <a href="#" class="button button--primary button--large">Submit</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  head() {
    return {
      bodyAttrs: {
        class: ['background-white'],
      },
    }
  },
}
</script>
