<template>
  <div class="w-full h-[260px]">
    <canvas ref="canvas" class="w-full h-full block"></canvas>
  </div>
</template>

<script>
import { nextTick } from "vue";
import Chart from "chart.js/auto";

export default {
  name: "VisitPieChart",
  props: {
    items: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      chart: null,
    };
  },
  watch: {
    items: {
      handler() {
        this.build();
      },
      deep: true,
    },
  },
  mounted() {
    this.build();
  },
  beforeUnmount() {
    this.teardown();
  },
  methods: {
    build() {
      nextTick(() => {
        const el = this.$refs.canvas;
        if (!el || !this.items || this.items.length === 0) {
          this.teardown();
          return;
        }

        const labels = this.items.map((i) => i.label);
        const data = this.items.map((i) => Number(i.value) || 0);
        const colors = this.colors(data.length);

        this.teardown();
        this.chart = new Chart(el.getContext("2d"), {
          type: "pie",
          data: {
            labels,
            datasets: [
              {
                data,
                backgroundColor: colors,
                borderWidth: 0,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { position: "bottom" },
            },
          },
        });
      });
    },
    teardown() {
      if (this.chart) {
        this.chart.destroy();
        this.chart = null;
      }
    },
    colors(n) {
      const base = [
        "#6C7A89",
        "#F5B041",
        "#A569BD",
        "#48C9B0",
        "#E74C3C",
        "#3498DB",
        "#58D68D",
        "#F4D03F",
      ];
      return Array.from({ length: n }, (_, i) => base[i % base.length]);
    },
  },
};
</script>
