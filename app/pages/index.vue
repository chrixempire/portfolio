<template>
  <DraftFrame>
    <section id="about" class="intro" aria-labelledby="name">
      <img
        class="portrait"
        src="/images/portrait.jpeg"
        alt=""
        width="56"
        height="56"
      >
      <h1 id="name" class="name">{{ site.name }}</h1>
      <p class="role">{{ site.title }} · {{ site.location }}</p>
      <p class="prose">
        I build the interface and stay with it through production. Most of that work has been fintech, procurement, SaaS, and marketplaces.
      </p>
      <p class="prose">
        I'm at Acumen Digital. Before that I led frontend at Independent Purchasing Company and helped the engineering team grow from 3 to 10. Alongside that I'm shipping Bayana, Quality, and PostHearts.
      </p>
      <p class="links">
        <a :href="site.gmail">Email</a>
        <a :href="site.socials[0].href" target="_blank" rel="noopener noreferrer">LinkedIn</a>
        <a :href="site.socials[1].href" target="_blank" rel="noopener noreferrer">GitHub</a>
        <a :href="site.resumeHref" download>Resume</a>
        <a :href="site.calendly" target="_blank" rel="noopener noreferrer">Schedule</a>
      </p>
    </section>

    <section id="work" class="block" aria-labelledby="work-label">
      <h2 id="work-label" class="label">Work</h2>
      <ol class="rows">
        <li v-for="(item, index) in products" :key="item.title">
          <component
            :is="linked(item) ? 'a' : 'div'"
            class="row"
            :href="linked(item) ? item.href : undefined"
            :target="item.external ? '_blank' : undefined"
            :rel="item.external ? 'noopener noreferrer' : undefined"
          >
            <span class="index">{{ String(index + 1).padStart(2, '0') }}</span>
            <span class="copy">
              <span class="title">
                {{ item.title }}
                <svg class="point" viewBox="0 0 16 16" aria-hidden="true">
                  <path d="M4.2 11.8 11.8 4.2M11.8 4.2H6.4M11.8 4.2v5.4" />
                </svg>
              </span>
              <span class="body">{{ roles[item.title] }}</span>
            </span>
            <img class="still" :src="item.poster" alt="" width="148" height="96">
          </component>
        </li>
      </ol>
    </section>

    <section id="experience" class="block" aria-labelledby="experience-label">
      <h2 id="experience-label" class="label">Experience</h2>
      <ol class="rows">
        <li v-for="job in experience" :key="job.role" class="job">
          <p class="when">{{ job.dates }}</p>
          <div class="copy">
            <p class="title">{{ job.role }}</p>
            <p class="body">{{ job.summary }}</p>
          </div>
        </li>
      </ol>
    </section>

    <footer id="hello" class="close">
      <p class="label">Say hello</p>
      <a class="mail" :href="site.gmail">{{ site.email }}</a>
      <p class="phone">{{ site.phoneDisplay }}</p>
    </footer>
    <SectionRail />
  </DraftFrame>
</template>

<script setup lang="ts">
import { site, products, experience } from '~/data/site'

useSiteSeo()

const roles: Record<string, string> = {
  GoSource: 'I built the website, the customer app, and the admin. Businesses order food through one procurement flow instead of chasing suppliers.',
  Kaorex: 'I built the trading interface. People exchange foreign currency with each other, with escrow, chat, and compliance in the same place.',
  Daash: 'I set the frontend direction and connected payments. A business runs its daily operations from one product.',
  Octupus: 'I built the market interface. People in Nigeria find prediction markets, browse categories, and follow what is moving.',
  Quality: 'I built the interface. Teams collect feedback and respond to it as it comes in.',
  PostHearts: 'I built the editor and the sharing flow. Someone writes a letter, designs it, and sends it from the web or a phone.',
  Bayana: 'I led the frontend. Verified NGOs post events and reach volunteers and donors.'
}

const linked = (item: { href: string }) => Boolean(item.href && item.href !== '#')
</script>
